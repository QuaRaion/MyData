import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import File
import pandas as pd
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@login_required
def render_files_page(request):
    user_files = File.objects.filter(user=request.user).order_by('-created_time')
    public_files = File.objects.filter(is_public=True).order_by('-created_time')

    form = UploadFileForm()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_instance = File.objects.create(
                name=form.cleaned_data.get('name') or uploaded_file.name,
                path=uploaded_file,
                user=request.user,
                separator=form.cleaned_data['separator'],
                has_header=form.cleaned_data['has_header'],
            )
            return redirect(reverse('edit_file', args=[file_instance.file_id]))

    return render(request, 'files/files_page.html', {
        'user_files': user_files,
        'public_files': public_files,
        'form': form,
    })


@login_required
def edit_headers(request, file_id):
    file_instance = File.objects.get(file_id=file_id)
    file_path = file_instance.path.path

    try:
        df = pd.read_csv(file_path, sep=file_instance.separator, encoding='utf-8')
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при чтении файла: {e}'}, status=400)

    if df.empty or df.columns.empty:
        return JsonResponse({'error': 'Файл не содержит данных или заголовков'}, status=400)

    df.columns = df.columns.str.strip()

    if request.method == 'POST':
        rename_mapping = {key.split('column_')[1]: value for key, value in request.POST.items() 
                          if key.startswith('column_') and value.strip()}

        for old_name in rename_mapping.keys():
            if old_name not in df.columns:
                return JsonResponse({'error': f'Столбец "{old_name}" не найден в данных'}, status=400)

        df.rename(columns=rename_mapping, inplace=True)

        dtype_mapping = {key.split('dtype_')[1]: value for key, value in request.POST.items() 
                         if key.startswith('dtype_')}

        for column, dtype in dtype_mapping.items():
            if column in df.columns:
                if dtype == 'int':
                    df[column] = pd.to_numeric(df[column], errors='coerce', downcast='integer')
                elif dtype == 'float':
                    df[column] = pd.to_numeric(df[column], errors='coerce', downcast='float')
                elif dtype == 'string':
                    df[column] = df[column].astype(str)
                elif dtype == 'bool':
                    df[column] = df[column].apply(lambda x: True if x in [1, '1', 'True', 'true', 'T', 't'] else False)
                    df[column] = df[column].astype(bool)
                elif dtype == 'date':
                    df[column] = pd.to_datetime(df[column], errors='coerce').dt.date
                elif dtype == 'datetime':
                    df[column] = pd.to_datetime(df[column], errors='coerce')


        columns_to_remove = [key.split('delete_')[1] for key, value in request.POST.items() if key.startswith('delete_')]
        df.drop(columns=columns_to_remove, errors='ignore', inplace=True)

        parquet_path = file_path.replace('.csv', '.parquet')
        try:
            df.to_parquet(parquet_path, engine='pyarrow', index=False)
            logger.info(f"Файл успешно сохранён в формате Parquet: {parquet_path}")
        except Exception as e:
            return JsonResponse({'error': f'Ошибка при сохранении файла в Parquet: {e}'}, status=400)

        return redirect('handle_duplicates', file_id=file_id)

    columns_and_types = zip(df.columns, df.dtypes.apply(str))
    return render(request, 'files/edit_headers.html', {'columns_and_types': columns_and_types, 'file_id': file_id})


@login_required
def handle_duplicates(request, file_id):
    file_instance = File.objects.get(file_id=file_id)
    file_path = file_instance.path.path.replace('.csv', '.parquet')

    try:
        df = pd.read_parquet(file_path, engine='pyarrow')
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")
        return JsonResponse({'error': 'Не удалось загрузить файл'}, status=500)

    if request.method == 'POST':
        if 'remove_explicit_duplicates' in request.POST:
            df = df.drop_duplicates()

        if 'implicit_values' in request.POST:
            implicit_values = json.loads(request.POST['implicit_values'])
            for item in implicit_values:
                col_name = item['column']
                new_value = item['new_value']
                df[col_name] = df[col_name].replace(item['old_value'], new_value)

        try:
            df.to_parquet(file_path, engine='pyarrow', index=False)
            logger.info(f"Файл успешно сохранён в Parquet: {file_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении файла: {e}")
            return JsonResponse({'error': f'Ошибка при сохранении файла: {e}'}, status=400)

        return redirect('files')

    explicit_duplicates = df[df.duplicated(keep=False)].reset_index().values.tolist()
    string_columns = df.select_dtypes(include=['object']).columns.tolist()

    return render(request, 'files/handle_duplicates.html', {
        'explicit_duplicates': explicit_duplicates,
        'string_columns': string_columns,
        'file_id': file_id,
    })


@csrf_exempt
def check_implicit_duplicates(request, file_id):
    body = json.loads(request.body)
    selected_columns = body.get('columns', [])

    file_instance = File.objects.get(file_id=file_id)
    file_path = file_instance.path.path.replace('.csv', '.parquet')

    try:
        df = pd.read_parquet(file_path, engine='pyarrow')
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")
        return JsonResponse({'error': 'Не удалось загрузить файл'}, status=500)

    if not selected_columns:
        return JsonResponse({'error': 'Не выбраны столбцы для проверки'}, status=400)

    missing_columns = [col for col in selected_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({'error': f"Не найдены столбцы: {', '.join(missing_columns)}"}, status=400)

    unique_values = [
        {'name': col, 'values': df[col].unique().tolist()} for col in selected_columns
    ]

    return JsonResponse({'unique_values': unique_values})

# SELECT column_name, data_type 
# FROM information_schema.columns 
# WHERE table_name = 'data';
