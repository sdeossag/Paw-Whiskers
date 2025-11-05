from django.urls import path
from . import views

urlpatterns = [
    path('', views.realizar_pedido, name="realizar_pedido"),
    path('reporte/', views.reporte_pedidos, name='reporte_pedidos'),
    path('reporte/cambiar-estado/<int:pedido_id>/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('reporte/exportar-csv/', views.exportar_pedidos_csv, name='exportar_pedidos_csv'),
    path('reporte/exportar-pdf/', views.exportar_pedidos_pdf, name='exportar_pedidos_pdf'),  # ✅ nueva ruta
]
