from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
def render_home_page(request):
    return render(request, 'main/home_page.html')
