from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_files_page, name='files'),
    # path('upload_file', views.render_upload_file_page, name='upload_file'),
]
