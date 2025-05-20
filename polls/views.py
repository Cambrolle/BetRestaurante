from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistroForm, LoginForm, ProductoForm, EmpleadoForm
from .models import User, Mesa, Producto


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

def camarero_page(request):
    return render(request, 'camarero.html')

def carta_page(request):
    return render(request, 'carta.html')
def camarero_page(request):
    return render(request, 'camarero.html')

def administrador_page(request):
    return render(request, 'administrar.html')

def mesas_page(request):
    mesas = Mesa.objects.all().order_by('codigo')
    return render(request, 'mesas.html', {'mesas': mesas})
def carta_view(request):
    productos = Producto.objects.all().order_by('id')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carta')
    else:
        form = ProductoForm()

    return render(request, 'carta.html', {'productos': productos, 'form': form})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('carta')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        return redirect('carta')

    return render(request, 'confirmar_eliminar.html', {'producto': producto})


def cambiar_estado_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    if request.method == 'POST':
        if mesa.disponibilidad == 'DISPONIBLE':
            mesa.disponibilidad = 'OCUPADO'
        else:
            mesa.disponibilidad = 'DISPONIBLE'
        mesa.save()
    return redirect('mesas')


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

def registrar_admin(request):
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
            email = form.cleaned_data.get('username')  # LoginForm usa 'username' para email por defecto
            password = form.cleaned_data.get('password')

            usuario = authenticate(request, email=email, password=password)

            if usuario is not None:
                login(request, usuario)

                # Redirige según el rol del usuario
                if usuario.rol == 'camarero':
                    return redirect('camarero_page')
                elif usuario.rol == 'admin':
                    return redirect('admin_page')
                elif usuario.rol == 'cliente':
                    return redirect('home')
                else:
                    return redirect('home')  # Fallback

            messages.error(request, "Correo electrónico o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'iniciar_sesion.html', {
        'form': form,
        'title': 'Iniciar Sesión'
    })


def empleados_view(request):
    empleados = User.objects.filter(rol__in=['camarero', 'cocinero']).order_by('nombre')

    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            nuevo_empleado = form.save(commit=False)
            nuevo_empleado.set_password(form.cleaned_data['password'])  # Encriptar contraseña
            nuevo_empleado.save()
            return redirect('empleados')
    else:
        form = EmpleadoForm()

    return render(request, 'admin_users.html', {'form': form, 'empleados': empleados})

def editar_empleado(request, id):
    empleado = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save(commit=False)
            if form.cleaned_data['password']:
                empleado.set_password(form.cleaned_data['password'])
            empleado.save()
            return redirect('empleados')
    else:
        form = EmpleadoForm(instance=empleado)
        form.fields['password'].initial = ''

    return render(request, 'editar_empleado.html', {'form': form})

def eliminar_empleado(request, id):
    empleado = get_object_or_404(User, id=id)

    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados')

    return render(request, 'confirmar_eliminar_empleado.html', {'empleado': empleado})



def logout_usuario(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('iniciar')





