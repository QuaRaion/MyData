from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import File
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def render_files_page(request):
    files = File.objects.filter(user=request.user).order_by('-created_time')
    return render(request, 'files/files_page.html', {'files':files})


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        separator = request.POST.get('separator')
        has_header = 'has_header' in request.POST

        try:
            df = pd.read_csv(file, sep=separator, header=0 if has_header else None)
            file_obj = File.objects.create(
                user=request.user,
                name=file.name,
                path=file,
                separator=separator,
                has_header=has_header
            )
            file_obj.save()

            return redirect('rename_columns', file_id=file_obj.file_id)

        except Exception as e:
            return HttpResponse(f"Ошибка загрузки файла: {str(e)}", status=400)
    
    return render(request, 'files/upload_file.html')

def rename_columns(request, file_id):
    file_obj = File.objects.get(file_id=file_id)
    df = pd.read_csv(file_obj.path.path, sep=file_obj.separator, header=0 if file_obj.has_header else None)

    if request.method == 'POST':
        # Получаем новые названия столбцов из формы
        renamed_columns = request.POST.getlist('columns')
        df.columns = renamed_columns
        # Сохраняем переименованные столбцы обратно в файл
        df.to_csv(file_obj.path.path, index=False)
        
        return redirect('check_data', file_id=file_obj.file_id)

    columns = df.columns.tolist()
    return render(request, 'files/rename_columns.html', {'columns': columns, 'file_id': file_id})


def check_data(request, file_id):
    file_obj = File.objects.get(file_id=file_id)
    df = pd.read_csv(file_obj.path.path, sep=file_obj.separator, header=0 if file_obj.has_header else None)

    if request.method == 'POST':
        if 'drop_nulls' in request.POST:
            df = df.dropna()  # Удаляем строки с пропусками
        elif 'remove_duplicates' in request.POST:
            df = df.drop_duplicates()  # Удаляем явные дубликаты

        # Сохраняем очищенные данные обратно в файл
        df.to_csv(file_obj.path.path, index=False)

        return redirect('change_data_types', file_id=file_obj.file_id)

    return render(request, 'files/check_data.html', {'data': df.to_html(classes='table'), 'file_id': file_id})

def change_data_types(request, file_id):
    file_obj = File.objects.get(file_id=file_id)
    df = pd.read_csv(file_obj.path.path, sep=file_obj.separator, header=0 if file_obj.has_header else None)

    if request.method == 'POST':
        data_types = {}
        for column in df.columns:
            dtype = request.POST.get(column)
            if dtype:
                data_types[column] = dtype
                df[column] = df[column].astype(dtype)

        # Сохраняем изменения в файл
        df.to_csv(file_obj.path.path, index=False)

        return redirect('save_file', file_id=file_obj.file_id)

    return render(request, 'files/change_data_types.html', {'columns': df.columns.tolist(), 'file_id': file_id})


def save_file(request, file_id):
    file_obj = File.objects.get(file_id=file_id)
    df = pd.read_csv(file_obj.path.path, sep=file_obj.separator, header=0 if file_obj.has_header else None)

    # Применяем окончательные изменения (например, типы данных)
    df.to_csv(file_obj.path.path, index=False)  # Финальный сохранённый файл

    return render(request, 'files/save_file.html', {'file_id': file_obj.file_id})

