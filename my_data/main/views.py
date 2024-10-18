from django.shortcuts import render


def render_home_page(request):
    return render(request, 'main/home_page.html')

def render_files_page(request):
    return render(request, 'main/files_page.html')

def render_chars_page(request):
    return render(request, 'main/charts_page.html')

def render_dashboards_page(request):
    return render(request, 'main/dashboards_page.html')

