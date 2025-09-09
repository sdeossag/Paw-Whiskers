from django.urls import path
from . import views

urlpatterns = [
    # URLs del Carrito
    path('', views.ver_carrito, name="ver_carrito"),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name="agregar_carrito"),
    path('restar/<int:producto_id>/', views.restar_carrito, name="restar_carrito"),
    path('eliminar/<int:item_id>/', views.eliminar_item_carrito, name="eliminar_item_carrito"),

    # URLs de Favoritos
    path('favoritos/', views.ver_favoritos, name='ver_favoritos'),
    path('favoritos/agregar/<int:producto_id>/', views.agregar_favorito, name='agregar_favorito'),
    path('favoritos/eliminar/<int:producto_id>/', views.eliminar_favorito, name='eliminar_favorito'),
    path('favoritos/mover-a-carrito/<int:producto_id>/', views.mover_favorito_a_carrito, name='mover_favorito_a_carrito'),
]
