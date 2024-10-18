from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('files', views.render_files_page, name='files'),
    path('charts', views.render_chars_page, name='charts'),
    path('dashboards', views.render_dashboards_page, name='dashboards'),
]
