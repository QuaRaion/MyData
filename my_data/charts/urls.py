from django.urls import path, include
from django_plotly_dash.views import add_to_session
from . import views
# from .views import NewChart

urlpatterns = [
    path('', views.render_charts_page, name='charts'),
    path('error/', views.render_error_page, name='error'),
    # path('<int:pk>/', NewChart.as_view(), name='create_chart'),
    path('<int:pk>/', views.create_chart_page, name='create_chart'),
    # path('save_chart/', views.save_chart, name='save_chart'),
]
