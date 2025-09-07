from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name="ver_carrito"),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name="agregar_carrito"),
    path('eliminar/<int:item_id>/', views.eliminar_item_carrito, name="eliminar_item_carrito"),
]
