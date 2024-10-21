from django.shortcuts import render

def render_dashboards_page(request):
    return render(request, 'dashboards/dashboards_page.html')

