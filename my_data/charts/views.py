from django.shortcuts import render, get_object_or_404
from files.models import File, DefaultFile
from django.views.generic import DetailView
from django.db import connection
import pandas as pd


def render_charts_page (request):
    files = File.objects.order_by('-created_time')
    default_files = DefaultFile.objects.order_by('name')
    return render(request, 'charts/charts_page.html', {'files':files, 'default_files':default_files})

class NewChart(DetailView):
    model = File
    template_name = 'charts/create_chart_page.html'
    context_object_name = 'file'

    def get(self, request, pk):
    # Получаем объект файла
        file = get_object_or_404(File, file_id=pk)

        # Читаем файл с учётом разделителя
        try:
            df = pd.read_csv(file.path.path, sep=file.separator, header=0 if file.has_header else None)
        except Exception as e:
            return render(request, 'error.html', {'message': f'Ошибка чтения файла: {e}'})

        # Получаем названия столбцов
        columns = list(df.columns)

        # Передаём данные в шаблон
        return render(request, 'charts/create_chart_page.html', {'columns': columns, 'file_name': file.name})

    
    # фильтр на файлы, принадлежащие пользователю 
    # def get_queryset(self):
    #     return File.objects.filter(user=user)


def render_test_page(request):
    return render(request, 'charts/test.html')
