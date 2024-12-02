from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import RegisterUser
from .forms import LoginUserForm
from .models import *
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password, make_password


def render_log_in_page(request):
    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                
                is_password_correct = check_password(password, user.password)

                if is_password_correct:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error('password', 'Неверный логин или пароль')

            except User.DoesNotExist:
                form.add_error('email', 'Пользователь с таким email не зарегистрирован')

    return render(request, 'registration/log_in.html', {'form': form})


def render_sign_up_page(request):
    form = RegisterUser()

    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        reg_data = RegisterUser(request.POST)

        if password != password2:
            reg_data.add_error('password2', 'Пароли не совпадают')
            return render(request, 'registration/sign_up.html', {'form': reg_data})
        
        if User.objects.filter(email=email).exists():
            reg_data.add_error('email', 'Пользователь с такой почтой уже зарегистрирован')
            return render(request, 'registration/sign_up.html', {'form': reg_data})

        hashed_password = make_password(password)
        User.objects.create(email=email, name=name, password=hashed_password)
        return redirect('log_in')

    else:
        return render(request, 'registration/sign_up.html', {'form':form})

# class LoginUser(LoginView):
#     form_class = AuthenticationForm
#     template_name = 'registration/log_in.html'

#     def form_invalid(self, form):
#         form.add_error('username', 'Неверный логин или пароль')
#         return self.render_to_response(self.get_context_data(form=form))
    
#     def get_success_url(self):
#         return reverse_lazy('home') 
