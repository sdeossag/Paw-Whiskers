from django.utils.translation import gettext_lazy as translate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoItem, Favorito
from clientes.models import CuentaCliente, RegistroActividad
from productos.models import Producto


# 🛒 Vistas del Carrito
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

    # Crear o actualizar item del carrito
    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": 1}
    )
    if not created:
        item.cantidad += 1
        item.save()

    # Registrar actividad (solo clientes)
    if not request.user.is_superuser:
        RegistroActividad.objects.create(
            usuario=request.user,
            tipo_actividad="CARRITO",
            detalles=translate("Añadió %(producto)s al carrito") % {"producto": producto.nombre}
        )

    return redirect("ver_carrito")


@login_required
def restar_carrito(request, producto_id):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    carrito = get_object_or_404(Carrito, cliente=cliente)
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        item = CarritoItem.objects.get(carrito=carrito, producto=producto)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
    except CarritoItem.DoesNotExist:
        pass  # No hay nada que restar si el item no existe

    return redirect("ver_carrito")


@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    item.delete()
    return redirect("ver_carrito")


# 💛 Vistas de Favoritos
@login_required
def ver_favoritos(request):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    favoritos, _ = Favorito.objects.get_or_create(cliente=cliente)
    productos = favoritos.productos.all()
    return render(request, "carrito/favoritos.html", {"favoritos": favoritos, "productos": productos})


@login_required
def agregar_favorito(request, producto_id):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    favoritos, _ = Favorito.objects.get_or_create(cliente=cliente)
    producto = get_object_or_404(Producto, id=producto_id)
    favoritos.productos.add(producto)

    # Registrar actividad
    if not request.user.is_superuser:
        RegistroActividad.objects.create(
            usuario=request.user,
            tipo_actividad="FAVORITO",
            detalles=translate("Añadió %(producto)s a favoritos") % {"producto": producto.nombre}
        )

    return redirect(request.META.get("HTTP_REFERER", "listar_productos"))


@login_required
def eliminar_favorito(request, producto_id):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    favoritos = get_object_or_404(Favorito, cliente=cliente)
    producto = get_object_or_404(Producto, id=producto_id)
    favoritos.productos.remove(producto)
    return redirect("ver_favoritos")


@login_required
def mover_favorito_a_carrito(request, producto_id):
    # Primero, agregamos el producto al carrito
    agregar_carrito(request, producto_id)
    # Luego, lo eliminamos de favoritos
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    favoritos = get_object_or_404(Favorito, cliente=cliente)
    producto = get_object_or_404(Producto, id=producto_id)
    favoritos.productos.remove(producto)
    return redirect("ver_carrito")