"""
URL configuration for BetRestaurante project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from polls.views import *
from django.contrib import admin
from django.urls import path, include
from polls import views as polls_views
urlpatterns = [
    path('', include('polls.urls')),
    path('bet/', include('polls.urls')),
    # path('inicio/', home_page, name="home"),
    # path('base/', base_page, name="base"),
    # path('crear_cuenta/', registrar_usuario, name="crear"),
    # path('iniciar_sesion/', login_usuario, name="iniciar"),
    # path('cerrar_sesion/', logout_usuario, name="logout"),
    # path('pagina_gestion/', gestion_page, name="gestionar"),
    # path('mesas/', mesas_page, name="mesas"),
    # path('mesas/cambiar_estado/<int:mesa_id>/', cambiar_estado_mesa, name="cambiar_estado_mesa"),
]

urlpatterns = [

    path('', include('polls.urls')),  # Importante: incluye aquí tu app
    path('prohibido/', polls_views.prueba_403),  # para probar 403
]

# Handlers de errores personalizados
handler403 = 'BetRestaurante.views.handler403'
handler404 = 'BetRestaurante.views.handler404'
