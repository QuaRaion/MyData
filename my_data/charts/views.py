from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.db import connection
import pandas as pd
import pyarrow.parquet as pq
from django.contrib.auth.decorators import login_required
from files.models import *

@login_required
def render_charts_page (request):
    user_files = File.objects.filter(user=request.user).order_by('-created_time')
    public_files = File.objects.filter(is_public=True).order_by('-name')
    
    return render(request, 'charts/charts_page.html', {'user_files':user_files, 'public_files':public_files})

class NewChart(DetailView):
    model = File
    template_name = 'charts/create_chart_page.html'
    context_object_name = 'file'

    def get(self, request, pk):
        file = get_object_or_404(File, file_id=pk)

        try:
            df = pd.read_parquet(file.path.path)
        except Exception as e:
            return render(request, 'error', {'message': f'Ошибка чтения файла: {e}'})        
            
        columns = list(df.columns)

        return render(request, 'charts/create_chart_page.html', {'columns': columns, 'file_name': file.name})
    
    # фильтр на файлы, принадлежащие пользователю 
    # def get_queryset(self):
    #     return File.objects.filter(user=user)


def render_error_page(request):
    return render(request, 'charts/error_page.html')
