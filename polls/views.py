from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import User


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home_page(request):
    return render(request, 'inicio.html')


def base_page(request):
    return render(request, 'base.html')


def gestion_page(request):
    return render(request, 'gestion.html')


def iniciar_page(request):
    return render(request, 'iniciar_sesion.html')


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, "¡Registro exitoso! Por favor inicia sesión.")
            return redirect('iniciar')
    else:
        form = RegistroForm()

    return render(request, 'crear_cuenta.html', {
        'form': form,
        'title': 'Crear Cuenta'
    })


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(request, email=email, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
        messages.error(request, "Correo electrónico o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'iniciar_sesion.html', {
        'form': form,
        'title': 'Iniciar Sesión'
    })


def logout_usuario(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('iniciar')


