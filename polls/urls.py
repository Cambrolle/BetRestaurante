from django.urls import path
from . import views
from .views import carta_view

urlpatterns = [
    path('', views.home_page, name="home"),
    path('inicio/', views.home_page, name="home"),
    path('base/', views.base_page, name="base"),
    path('crear_cuenta/', views.registrar_usuario, name="crear"),
    path('iniciar_sesion/', views.login_usuario, name="iniciar"),
    path('cerrar_sesion/', views.logout_usuario, name="logout"),
    path('pagina_gestion/', views.gestion_page, name="gestionar"),
    path('pagina_camarero/', views.camarero_page, name="camarero_page"),
    path('pagina_carta/', views.carta_page, name="carta"),
    path('admin/', views.administrador_page, name="admin_page"),
    path('mesas/cambiar_estado/<int:mesa_id>/', views.cambiar_estado_mesa, name="cambiar_estado_mesa"),
    path('mesas/', views.mesas_page, name="mesas"),
    path('carta/', views.carta_view, name='carta'),
    path('producto/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('empleados/', views.empleados_view, name='empleados'),
    path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),

    path('carta_camarero/', views.vista_carta_camarero, name='vista_carta_camarero'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('procesar_pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('carrito/enviar/', views.enviar_pedido, name='enviar_pedido'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('modificar_carrito/', views.modificar_carrito, name='modificar_carrito'),

]

