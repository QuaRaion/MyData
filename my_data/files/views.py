from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse
import pandas as pd
from django.contrib.auth.decorators import login_required

from .models import File
from .forms import UploadFileForm


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
def render_edit_file_page(request, file_id):
    file_instance = File.objects.get(file_id=file_id)

    # Логика обработки файла
    file_path = file_instance.path.path
    df = pd.read_csv(file_path, sep=file_instance.separator, header=0 if file_instance.has_header else None)

    # Пример отображения первых строк файла
    preview = df.head().to_html()

    return render(request, 'files/edit_file.html', {
        'file': file_instance,
        'preview': preview,
    })



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

