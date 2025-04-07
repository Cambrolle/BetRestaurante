from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', home_page, name="home"),
    path('inicio/', home_page, name="home"),
    path('base/', base_page, name="base"),
    path('crear_cuenta/', crear_page, name="crear"),
    path('iniciar_sesion/', iniciar_page, name="iniciar"),
]