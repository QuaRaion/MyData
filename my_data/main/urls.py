from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.render_home_page, name='home'),
    # path('', include('registration.urls')),
    path('files/', include('files.urls')),
    path('charts/', include('charts.urls')),
    path('dashboards/', include('dashboards.urls')),
]
