from django import forms


class UploadFileForm(forms.Form):
    name = forms.CharField(
        label=None,
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'text-h3 text-black',
            'placeholder': 'Имя файла',
            'autocomplete': 'off'
        })
    )
    file = forms.FileField(
        label='Выбрать файл',
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'button upload-btn hidden',
            'accept': '.csv,.xls,.xlsx',
        })
    )
    separator = forms.CharField(
        max_length=5,
        label='Разделитель',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'sep_input text-h3 text-black',
            'placeholder': '',
            'autocomplete': 'off'
        })
    )
    has_header = forms.BooleanField(
        label='Файл содержит заголовки',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'text-h3 text-black',
        })
    )

