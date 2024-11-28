from django.shortcuts import render

def render_log_in_page (request):
    return render(request, 'registration/login.html')

def render_sign_up_page (request):
    return render(request, 'registration/register.html')

