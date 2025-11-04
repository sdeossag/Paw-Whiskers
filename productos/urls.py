from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_productos, name="listar_productos"),
    path('<int:producto_id>/', views.detalle_producto, name="detalle_producto"),
    path("agregar-excel/", views.agregar_productos_excel, name="agregar_productos_excel"),

    # Panel administrador (usa la misma vista pero protegido en el template con {% if user.is_superuser %})
    path("admin/productos/", views.listar_productos, name="lista_productos"),
    path("admin/productos/crear/", views.crear_producto, name="crear_producto"),
    path("admin/productos/<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("admin/productos/<int:pk>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
    path("admin/productos/restablecer-stock/", views.restablecer_stock, name="restablecer_stock"),

    # API
    path("api/productos-en-stock/", views.productos_en_stock_api, name="productos_en_stock_api"),
]