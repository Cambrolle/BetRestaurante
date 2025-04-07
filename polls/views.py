from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def home_page(request):
    return render(request, 'inicio.html')
def base_page(request):
    return render(request, 'base.html')

def crear_page(request):
    return render(request, 'crear_cuenta.html')