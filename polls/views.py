from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistroForm, LoginForm
from .models import User



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def home_page(request):
    return render(request, 'inicio.html')
def base_page(request):
    return render(request, 'base.html')

def crear_page(request):
    return render(request, 'crear_cuenta.html')
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
            return redirect('iniciar')
        else:
            form = RegistroForm()
        return render(request, 'usuarios/crear_cuenta.html', {'form': form})
