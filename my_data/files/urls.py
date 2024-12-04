from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_files_page, name='files'),
    path('edit/<int:file_id>/', views.edit_headers, name='edit_file'),
    path('duplicates/<int:file_id>/', views.handle_duplicates, name='handle_duplicates'),
    path('check_duplicates/<int:file_id>/', views.check_implicit_duplicates, name='check_implicit_duplicates'),
]
