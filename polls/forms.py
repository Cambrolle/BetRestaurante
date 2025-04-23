from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'nombre', 'rol', 'password']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo")