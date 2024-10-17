from django.shortcuts import render


def create_chart(request):
    return render(request, 'main/charts_page.html')
