from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Pedido
from clientes.models import CuentaCliente, RegistroActividad
from carrito.models import Carrito
from django.http import HttpResponse

# Inversión de Dependencias: Importamos las clases desde el nuevo módulo
from .report_generators import ReporteExcelGenerator, ReportePDFGenerator


# Decorador para vistas de administrador
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@login_required
def realizar_pedido(request):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    try:
        carrito = Carrito.objects.get(cliente=cliente)
        items = carrito.carritoitem_set.all()
    except Carrito.DoesNotExist:
        return redirect('ver_carrito')

    if not items.exists():
        messages.info(request, _("Tu carrito está vacío. Añade productos antes de realizar un pedido."))
        return redirect('ver_carrito')

    if request.method == _("GET"):
        for item in items:
            if item.cantidad > item.producto.cantidadDisp:
                messages.error(request, f"Stock insuficiente para '{item.producto.nombre}'. Disponible: {item.producto.cantidadDisp}, en carrito: {item.cantidad}.")
                return redirect('ver_carrito')

    if request.method == _("POST"):
        for item in items:
            if item.cantidad > item.producto.cantidadDisp:
                messages.error(request, f"Mientras confirmabas, el stock para '{item.producto.nombre}' cambió. No se pudo completar el pedido.")
                return redirect('ver_carrito')

        pedido = Pedido.objects.create(
            cliente=cliente,
            total=carrito.total_carrito, # Corregido de totalPedido a total
            direccion_entrega=cliente.direccion # Corregido de direccionPedido a direccion_entrega
        )

        # Registrar actividad
        if not request.user.is_superuser:
            RegistroActividad.objects.create(
                usuario=request.user,
                tipo_actividad=_("PEDIDO"),
                detalles=f'Realizó el pedido #{pedido.id} por un total de ${pedido.total}'
            )
        
        for item in items:
            producto = item.producto
            producto.cantidadDisp -= item.cantidad
            producto.save()
        
        carrito.carritoitem_set.all().delete()
        
        messages.success(request, _("¡Simulación de pedido realizada con éxito!"))
        return redirect("home")

    context = {
        _("carrito"): carrito,
        _("items"): items
    }
    return render(request, "pedidos/pedido.html", context)


@admin_required
def reporte_pedidos(request):
    # Obtenemos el formato de la URL (?formato=excel o ?formato=pdf)
    formato = request.GET.get('formato')
    pedidos = Pedido.objects.all().order_by('-fechaPedido')

    # El módulo de alto nivel (la vista) depende de la abstracción (ReportGenerator)
    # y no de las implementaciones concretas.
    generador = None
    if formato == 'excel':
        generador = ReporteExcelGenerator() # Seleccionamos la implementación concreta
    elif formato == 'pdf':
        generador = ReportePDFGenerator() # Seleccionamos la otra implementación

    # Si se eligió un generador, lo usamos para devolver el archivo
    if generador:
        return generador.generate(pedidos)

    # Si no se especifica un formato, renderizamos la plantilla HTML
    return render(request, 'pedidos/reporte_pedidos.html', {'pedidos': pedidos})


@admin_required
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = nuevo_estado
    pedido.save()
    messages.success(request, f"El estado del pedido #{pedido.id} ha sido actualizado a '{nuevo_estado}'.")
    return redirect('reporte_pedidos')

