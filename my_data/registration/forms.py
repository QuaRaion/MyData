from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginUserForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'input text-black text-h3', 'placeholder': 'Электронная почта'})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'input text-black text-h3', 'placeholder': 'Пароль'})
    )


class RegisterUserForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'input text-black text-h3',
                                      'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(
        max_length=50, 
        widget=forms.EmailInput(attrs={'class': 'input text-black text-h3', 
                                       'placeholder': 'Электронная почта'}))
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'input text-black text-h3', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'input text-black text-h3', 'placeholder': 'Подтвердите пароль'}),
    )

    class Meta:
        model = User
        fields = ['name', 'email']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

