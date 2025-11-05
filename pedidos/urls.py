from django.urls import path
from . import views

urlpatterns = [
    path('', views.realizar_pedido, name="realizar_pedido"),
    path('reporte/', views.reporte_pedidos, name='reporte_pedidos'),
    path('reporte/cambiar-estado/<int:pedido_id>/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),

]
