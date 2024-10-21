from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from my_data import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('files/', include('files.urls')),
    path('charts/', include('charts.urls')),
    path('dashboards/', include('dashboards.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)