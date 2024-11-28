from django.urls import path, include
from django_plotly_dash.views import add_to_session
from . import views
from .views import NewChart

urlpatterns = [
    path('', views.render_charts_page, name='charts'),
    path('test/', views.render_test_page, name='test'),
    path('create_chart/<int:pk>/', NewChart.as_view(), name='create_chart'), 
]
