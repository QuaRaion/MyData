from django.shortcuts import render
from .models import File

def render_files_page(request):
    files = File.objects.order_by('-created_time')
    return render(request, 'files/files_page.html', {'files':files})
