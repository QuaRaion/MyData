from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('files/', include('files.urls'), name='files'),
    path('charts/', include('charts.urls'), name='charts'),
    path('dashboards/', include('dashboards.urls'), name='dashboards'),
]
