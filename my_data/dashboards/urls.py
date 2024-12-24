from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_dashboards_page, name='dashboards'),
    path('create_dashboard/', views.render_create_dashboard_page, name='create_dashboard'),
    path('<int:pk>/filters/', views.get_chart_filters, name='chart_filters'),
]
