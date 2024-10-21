from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('files/', include('files.urls')),
    path('charts/', include('charts.urls')),
    path('dashboards/', include('dashboards.urls'))
]
