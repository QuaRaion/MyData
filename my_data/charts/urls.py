from django.urls import path, include
from django_plotly_dash.views import add_to_session
from . import views
from .views import NewChart

urlpatterns = [
    path('', views.render_charts_page, name='charts'),
    path('error/', views.render_error_page, name='error'),
    # path('<int:pk>/', NewChart.as_view(), name='create_chart'),
    path('test/', views.index, name='index'),
]
