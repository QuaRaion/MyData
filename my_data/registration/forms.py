from django import forms
from .models import *


class LoginUserForm(forms.Form):
    email = forms.EmailField(max_length=50,
                             widget=forms.EmailInput(attrs={'class': 'input', 
                                                            'placeholder': 'Электронная почта'}))
    password = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'input', 
                                                                 'placeholder': 'Пароль'}))
    

class RegisterUser(forms.Form):
    name = forms.CharField(max_length=50, 
                           widget=forms.TextInput(attrs={'class': 'input', 
                                                         'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(max_length=50, 
                             widget=forms.EmailInput(attrs={'class': 'input', 
                                                            'placeholder': 'Электронная почта'}))
    password = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'input', 
                                                                 'placeholder': 'Пароль'}))
    password2 = forms.CharField(max_length=50, 
                                widget=forms.PasswordInput(attrs={'class': 'input', 
                                                                  'placeholder': 'Подтвердите пароль'}))
