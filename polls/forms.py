from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Producto


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'required': 'required'
        }),
        label="Contraseña",
        strip=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'required': 'required'
        }),
        label="Confirmar Contraseña",
        strip=False,
    )

    class Meta:
        model = User
        fields = ['email', 'nombre']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com',
                'required': 'required'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'required': 'required'
            }),

        }
        labels = {
            'email': 'Correo Electrónico',
            'nombre': 'Nombre Completo',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'autofocus': True,
            'required': 'required'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'required': 'required'
        }),
    )

    error_messages = {
        'invalid_login': "Correo electrónico o contraseña incorrectos.",
        'inactive': "Esta cuenta está inactiva.",
    }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['tipo', 'producto', 'descripcion', 'imagen', 'precio']

class RegistroAdmin(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'required': 'required'
        }),
        label="Contraseña",
        strip=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'required': 'required'
        }),
        label="Confirmar Contraseña",
        strip=False,
    )

    class Meta:
        model = User
        fields = ['email', 'nombre', 'rol']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com',
                'required': 'required'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'required': 'required'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Tu rol',
                'required': 'required'
            })

        }
        labels = {
            'email': 'Correo Electrónico',
            'nombre': 'Nombre Completo',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user