from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import RegisterUserForm, LoginUserForm


User = get_user_model()

def render_log_in_page(request):
    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'], 
                                password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('email', 'Неверная почта или пароль')

    return render(request, 'registration/log_in.html', {'form': form})


def render_sign_up_page(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('log_in')

    return render(request, 'registration/sign_up.html', {'form': form})


def privacy_policy(request):
    return render(request, 'registration/privacy_policy.html')

def agreement(request):
    return render(request, 'registration/agreement.html')