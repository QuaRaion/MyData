from django import forms


class UploadFileForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Электронная почта'})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Пароль'})
    )
