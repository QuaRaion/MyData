import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def render_dashboards_page(request):
    return render(request, 'dashboards/dashboards_page.html')


@login_required
def render_create_dashboard_page(request):
    charts = Chart.objects.filter(user=request.user)
    return render(request, 'dashboards/create_dashboard_page.html',  {'charts': charts})

@login_required
def save_dashboard(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        selected_charts = data.get('charts')
        positions = data.get('positions')

        dashboard = Dashboard.objects.create(user=request.user, name=name)
        dashboard.charts.set(Chart.objects.filter(id__in=selected_charts))
        dashboard.save()

        return JsonResponse({'message': 'Dashboard saved successfully', 'dashboard_id': dashboard.dashboard_id})
    return JsonResponse({'error': 'Invalid request'}, status=400)   


@login_required
def get_chart_filters(request, pk):
    chart = get_object_or_404(Chart, chart_id=pk, user=request.user)
    filters = chart.filters
    return JsonResponse({'filters': filters})
