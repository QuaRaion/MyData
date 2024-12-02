from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_files_page, name='files'),
    path('edit/<int:file_id>/', views.render_edit_file_page, name='edit_file'),
]
