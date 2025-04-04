from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', home_page, name="home"),
    path('home/', home_page, name="home"),
    path('base/', base_page, name="base"),
]