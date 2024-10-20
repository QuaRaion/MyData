from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import File
import pandas as pd

def render_home_page(request):
    file = get_object_or_404(File, file_id=1)
    csv_data = None
    
    try:
        csv_data = pd.read_csv(file.path, delimiter=';')
        print(csv_data)
    except Exception as e:
        print(f"Ошибка чтения файла! {e}")

    return render(request, 'main/home_page.html', {
        'file': file,
        'csv_data': csv_data,})


def render_files_page(request):
    return render(request, 'main/files_page.html')

def render_chars_page(request):
    return render(request, 'main/charts_page.html')

def render_dashboards_page(request):
    return render(request, 'main/dashboards_page.html')

