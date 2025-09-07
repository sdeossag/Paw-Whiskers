from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido
from clientes.models import CuentaCliente
from carrito.models import Carrito

@login_required
def realizar_pedido(request):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    carrito = get_object_or_404(Carrito, cliente=cliente)

    if request.method == "POST":
        pedido = Pedido.objects.create(
            cliente=cliente,
            totalPedido=carrito.totalCarrito,
            direccionPedido=cliente.direccionPedido
        )
        carrito.carritoitem_set.all().delete()
        carrito.totalCarrito = 0
        carrito.save()
        messages.success(request, "Pedido realizado con éxito")
        return redirect("listar_productos")

    return render(request, "pedidos/pedido.html", {"carrito": carrito})
