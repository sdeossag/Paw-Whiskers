from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('productos-aliados/', views.productos_aliados, name='productos_aliados'),
]
