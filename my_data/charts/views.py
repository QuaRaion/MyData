import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def render_charts_page (request):
    user_charts = Chart.objects.filter(user=request.user).order_by('-created_time')
    public_charts = Chart.objects.filter(is_public=True).order_by('-created_time')
    user_files = File.objects.filter(user=request.user).order_by('-created_time')
    public_files = File.objects.filter(is_public=True).order_by('-created_time')
    
    return render(request, 'charts/charts_page.html', 
                  {'user_files':user_files, 
                   'public_files':public_files,
                   'user_charts':user_charts, 
                   'public_charts':public_charts,})



def render_error_page(request, pk):
    p = pk
    return render(request, 'charts/error_page.html')


def create_chart_page(request, pk):
    file_instance = get_object_or_404(File, file_id=pk)

    try:
        df = pd.read_parquet(file_instance.path.path)
        data = df.to_dict(orient='records')
    except Exception as e:
        return render(request, 'charts/error_page.html', {'error': str(e)})

    return render(request, 'charts/create_chart_page.html', {
        'file_id': pk,
        'dataframe': data
    })


# реализация сохранения чарта в БД
def save_chart(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            chart_name = data.get('name')
            filters = data.get('filters')

            if not chart_name:
                return JsonResponse({'error': 'Название чарта обязательно!'}, status=400)

            file_instance = get_object_or_404(File, file_id=pk)

            # сохранение чарта в БД
            chart = Chart.objects.create(
                user=request.user,
                file=file_instance,
                name=chart_name,
                filters=filters
            )

            return JsonResponse({'message': 'Чарт успешно сохранен!', 'chart_id': chart.chart_id})
        
        except Exception as e:
            print(f"Ошибка: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Метод запроса не поддерживается'}, status=405)

