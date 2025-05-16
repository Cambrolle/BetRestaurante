from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('inicio/', views.home_page, name="home"),
    path('base/', views.base_page, name="base"),
    path('crear_cuenta/', views.registrar_usuario, name="crear"),
    path('iniciar_sesion/', views.login_usuario, name="iniciar"),
    path('cerrar_sesion/', views.logout_usuario, name="logout"),
    path('pagina_gestion/', views.gestion_page, name="gestionar"),
    path('pagina_camarero/', views.camarero_page, name="camarero"),
    path('pagina_carta/', views.carta_page, name="carta"),
]

