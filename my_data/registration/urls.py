from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_log_in_page, name='log_in'),
    path('/sign_up', views.render_sign_up_page, name='sign_up')
]
