from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoItem
from clientes.models import CuentaCliente
from productos.models import Producto

@login_required
def ver_carrito(request):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
    items = carrito.carritoitem_set.all()
    return render(request, "carrito/carrito.html", {"carrito": carrito, "items": items})

@login_required
def agregar_carrito(request, producto_id):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
    producto = get_object_or_404(Producto, id=producto_id)

    item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
    item.save()

    carrito.totalCarrito = sum(i.producto.precio * i.cantidad for i in carrito.carritoitem_set.all())
    carrito.save()
    return redirect("ver_carrito")

@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    carrito = item.carrito
    item.delete()
    carrito.totalCarrito = sum(i.producto.precio * i.cantidad for i in carrito.carritoitem_set.all())
    carrito.save()
    return redirect("ver_carrito")
