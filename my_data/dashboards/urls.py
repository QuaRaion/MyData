from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_dashboards_page, name='dashboards'),
]
