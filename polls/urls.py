from django.urls import path
from . import views
from .views import carta_view, confirmacion_pedido

urlpatterns = [
    path('', views.home_page, name="home"),
    path('inicio/', views.home_page, name="home"),
    path('base/', views.base_page, name="base"),
    path('crear_cuenta/', views.registrar_usuario, name="crear"),
    path('iniciar_sesion/', views.login_usuario, name="iniciar"),
    path('cerrar_sesion/', views.logout_usuario, name="logout"),
    path('pagina_gestion/', views.gestion_page, name="gestionar"),
    path('pagina_camarero/', views.camarero_page, name="camarero_page"),
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
    path('confirmacion-pedido/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('cocinero/', views.cocinero_page, name="cocinero"),
    path('pedidos/', views.vista_pedidos_cocinero, name="pedidos"),
    path('pedidos/marcar_preparado/<int:pedido_id>/', views.marcar_pedido_preparado, name='marcar_pedido_preparado'),
    path('admin/mesas/', views.mesas_admin, name='mesas_admin'),
    path('admin/mesas/agregar/', views.agregar_mesa, name='agregar_mesa'),
    path('admin/mesas/eliminar/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa'),
    path('camarero/pedidos/', views.ver_pedidos_realizados, name='ver_pedidos_realizados'),
    path('camarero/editar-pedidos/', views.editar_pedidos_realizados, name='editar_pedidos_realizados'),
    path('historial/', views.historial_pedidos_cliente, name='historial_pedidos'),
    path('admin/pedidos/', views.vista_pedidos_admin, name='pedidos_admin'),

]




