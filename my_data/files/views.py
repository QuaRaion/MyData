from django.shortcuts import render
from .models import File

def render_files_page(request):
    file = File.objects.order_by('-created_time')
    return render(request, 'files/files_page.html', {'file':file})
