from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('productos/', views.listar_productos, name="listar_productos"),
    path('producto/<int:producto_id>/', views.detalle_producto, name="detalle_producto"),
    path('carrito/', views.ver_carrito, name="ver_carrito"),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name="agregar_carrito"),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item_carrito, name="eliminar_item_carrito"),
    path('pedido/', views.realizar_pedido, name="realizar_pedido"),

    # 🔑 rutas de login/logout
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path("agregar-productos-excel/", views.agregar_productos_excel, name="agregar_productos_excel"),

]
