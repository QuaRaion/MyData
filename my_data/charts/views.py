from django.shortcuts import render
from files.models import File, DefaultFile
from django.views.generic import DetailView

def render_charts_page (request):
    files = File.objects.order_by('-created_time')
    default_files = DefaultFile.objects.order_by('name')
    return render(request, 'charts/charts_page.html', {'files':files, 'default_files':default_files})

class NewChart(DetailView):
    model = File
    template_name = 'charts/create_chart_page.html'
    context_object_name = 'file'
    
    # фильтр на файлы, принадлежащие пользователю 
    # def get_queryset(self):
    #     return File.objects.filter(user=user)

