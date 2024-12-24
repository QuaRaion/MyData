from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from my_data import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registration.urls')),
    
    # подключение django_plotly_dash
    # path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)