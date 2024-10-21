from django.shortcuts import render

def render_charts_page (request):
    return render(request, 'charts/charts_page.html')