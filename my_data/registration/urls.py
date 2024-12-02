from django.urls import include, path
from . import views

urlpatterns = [
    path('log_in/', views.render_log_in_page, name='log_in'),
    path('', views.render_sign_up_page, name='sign_up'),
    path('home/', include('main.urls'), name='home'),
]
