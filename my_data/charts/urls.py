from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_charts_page, name='charts'),
]
