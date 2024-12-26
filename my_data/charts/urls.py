from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.render_charts_page, name='charts'),
    path('error/', views.render_error_page, name='error'),
    path('<int:pk>/', views.create_chart_page, name='create_chart'),
    path('<int:pk>/save/', views.save_chart, name='save_chart'),
]
