from django.urls import path
from . import views
from .views import NewChart

urlpatterns = [
    path('', views.render_charts_page, name='charts'),
    path('create_chart/<int:pk>/', NewChart.as_view(), name='create_chart'), 
]
