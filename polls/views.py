from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import time
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import RegistroForm, LoginForm, ProductoForm, EmpleadoForm
from .models import User, Mesa, Producto, Carrito, ItemCarrito, PedidoItem

from .models import Pedido



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

def cocinero_page(request):
    return render(request, 'cocinero.html')

def administrador_page(request):
    return render(request, 'administrar.html')

def mesas_page(request):
    mesas = Mesa.objects.all().order_by('codigo')
    return render(request, 'mesas.html', {'mesas': mesas})

def confirmacion_pedido(request):
    return render(request, 'confirmacion_pedido.html')
from django.shortcuts import render

def vista_pedidos_cocinero(request):
    pedidos = Pedido.objects.filter(estado='PENDIENTE').order_by('fecha_creacion')
    return render(request, 'pedidos_cocinero.html', {'pedidos': pedidos})



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
                elif usuario.rol == 'cocinero':
                    return redirect('cocinero')
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



def vista_carta_camarero(request):
    mesas = Mesa.objects.filter(disponibilidad='OCUPADO')

    mesa_id = request.GET.get('mesa_id')
    if mesa_id:
        # Guardar mesa en sesión
        if "carrito" not in request.session:
            request.session["carrito"] = {}
        request.session["carrito"]["mesa_id"] = mesa_id
        request.session.modified = True
    else:
        # Si no está en GET, intentar recuperar de la sesión
        mesa_id = request.session.get("carrito", {}).get("mesa_id")

    productos = Producto.objects.all()
    carrito = request.session.get('carrito', {})
    items = []
    total = 0

    # Aseguramos que carrito tenga 'items' y que la mesa coincida
    if carrito and str(mesa_id) == str(carrito.get('mesa_id')) and 'items' in carrito:
        for item in carrito['items']:
            subtotal = item['precio'] * item['cantidad']
            total += subtotal
            items.append({
                'producto_id': item['id'],
                'producto': {'producto': item['nombre']},  # Aquí nombre del producto
                'cantidad': item['cantidad'],
                'precio_unitario': item['precio'],
                'subtotal': subtotal,
            })

    context = {
        'mesas': mesas,
        'mesa_id': mesa_id,
        'productos': productos,
        'items': items,
        'total': total,
    }

    return render(request, 'carta_camarero.html', context)





@require_POST
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    # Inicializa el carrito si no existe en la sesión
    if 'carrito' not in request.session:
        request.session['carrito'] = {'items': []}

    carrito = request.session['carrito']
    items = carrito.get('items', [])

    # Verifica si el producto ya está en el carrito
    for item in items:
        if item['id'] == producto.id:
            item['cantidad'] += 1
            break
    else:
        # Si no está, lo agregamos
        items.append({
            'id': producto.id,
            'nombre': producto.producto,  # <-- campo correcto
            'precio': float(producto.precio),
            'cantidad': 1,
        })

    # Guarda los cambios
    carrito['items'] = items
    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect('vista_carta_camarero')  # Cambia esto si tu vista tiene otro nombre

@login_required
def procesar_pedido(request):
    carrito = get_object_or_404(Carrito, camarero=request.user, mesa__disponibilidad='OCUPADO')
    if carrito.items.exists():
        pedido = Pedido.objects.create(
            codigo=f"PED-{carrito.id}",
            cliente=None,
            camarero=request.user,
            cocinero=None
        )
        for item in carrito.items.all():
            Pedido.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.precio_unitario,
                estado_producto='PENDIENTE'
            )
        carrito.delete()
        return redirect('vista_carta_camarero')
    else:
        return redirect('vista_carta_camarero')
@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', None)

    if not carrito or not carrito.get('items'):
        messages.info(request, "El carrito está vacío.")
        return redirect('vista_carta_camarero')

    items = carrito['items']

    # Construir lista de productos con subtotal
    productos_carrito = []
    total_general = 0

    for prod_id_str, item in items.items():
        subtotal = item['precio'] * item['cantidad']
        total_general += subtotal
        productos_carrito.append({
            'id': prod_id_str,
            'nombre': item['producto'],
            'precio': item['precio'],
            'cantidad': item['cantidad'],
            'subtotal': subtotal,
        })

    context = {
        'mesa_id': carrito.get('mesa_id'),
        'productos_carrito': productos_carrito,
        'total_general': total_general,
    }
    return render(request, 'polls/ver_carrito.html', context)
@require_POST
@login_required
def eliminar_item_carrito(request, producto_id):
    carrito = request.session.get('carrito', None)
    if carrito and 'items' in carrito and str(producto_id) in carrito['items']:
        del carrito['items'][str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito.")
    else:
        messages.error(request, "Producto no encontrado en el carrito.")

    return redirect('ver_carrito')


def enviar_pedido(request):
    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        if not mesa_id:
            return redirect('carta_camarero')

        try:
            mesa = Mesa.objects.get(id=int(mesa_id))
        except Mesa.DoesNotExist:
            return redirect('carta_camarero')

        carrito = request.session.get('carrito', {})
        if not carrito or 'items' not in carrito:
            return redirect('carta_camarero')

        # Crear un solo Pedido para esa mesa
        pedido = Pedido.objects.create(
            mesa=mesa,
            estado='PENDIENTE'
        )

        # Guardar todos los productos del carrito como PedidoItem relacionados al Pedido
        for item in carrito['items']:
            producto_id = item.get('id')
            cantidad = item.get('cantidad', 1)
            precio_unitario = item.get('precio', 0)
            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                continue

            PedidoItem.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )

        # Limpiar carrito
        if 'carrito' in request.session:
            del request.session['carrito']

        return redirect('confirmacion_pedido')

    return redirect('carta_camarero')



@login_required
def vista_pedidos_cocinero(request):
    pedidos = Pedido.objects.filter(cocinero=None)
    return render(request, 'pedidos_cocinero.html', {'pedidos': pedidos})

@require_POST
@login_required
def marcar_pedido_preparado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'PREPARANDO'  # O 'LISTO' según lo que quieras
    pedido.cocinero = request.user
    pedido.save()
    return redirect('pedidos')
@require_POST
def modificar_carrito(request):
    producto_id = int(request.POST.get("producto_id"))
    accion = request.POST.get("accion")
    mesa_id = request.session.get("carrito", {}).get("mesa_id")

    carrito = request.session.get("carrito", {})

    # Si no hay items, inicializar lista vacía
    if "items" not in carrito or not isinstance(carrito["items"], list):
        carrito["items"] = []

    items = carrito["items"]

    # Buscar el item en la lista por id
    item_encontrado = None
    for item in items:
        if item['id'] == producto_id:
            item_encontrado = item
            break

    if not item_encontrado:
        messages.error(request, "El producto no está en el carrito.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if accion == "incrementar":
        item_encontrado["cantidad"] += 1
        messages.success(request, "Cantidad incrementada.")

    elif accion == "disminuir":
        if item_encontrado["cantidad"] > 1:
            item_encontrado["cantidad"] -= 1
            messages.success(request, "Cantidad disminuida.")
        else:
            items.remove(item_encontrado)
            messages.success(request, "Producto eliminado del carrito.")

    elif accion == "eliminar":
        items.remove(item_encontrado)
        messages.success(request, "Producto eliminado del carrito.")

    # Guardar cambios en sesión
    carrito["items"] = items
    request.session["carrito"] = carrito
    request.session.modified = True

    # Redirigir a la carta con mesa_id en la URL
    if mesa_id:
        return redirect(f"/carta_camarero/?mesa_id={mesa_id}")
    else:
        return redirect("vista_carta_camarero")






