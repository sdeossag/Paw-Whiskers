from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Pedido
from clientes.models import CuentaCliente, RegistroActividad
from carrito.models import Carrito

# Importar las clases de inversión de dependencias
from .exporters import ReporteService, CSVExporter, PDFExporter


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
            totalPedido=carrito.total_carrito,
            direccionPedido=cliente.direccionPedido
        )

        # Registrar actividad
        if not request.user.is_superuser:
            RegistroActividad.objects.create(
                usuario=request.user,
                tipo_actividad=_("PEDIDO"),
                detalles=f'Realizó el pedido #{pedido.id} por un total de ${pedido.totalPedido}'
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
    pedidos = Pedido.objects.all().order_by('-fechaPedido')
    return render(request, 'pedidos/reporte_pedidos.html', {'pedidos': pedidos})


@admin_required
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = nuevo_estado
    pedido.save()
    messages.success(request, f"El estado del pedido #{pedido.id} ha sido actualizado a '{nuevo_estado}'.")
    return redirect('reporte_pedidos')


# ============================================================
# VISTAS CON INVERSIÓN DE DEPENDENCIAS
# ============================================================

@admin_required
def exportar_pedidos_csv(request):
    """
    Exporta pedidos a CSV utilizando inversión de dependencias.
    El módulo de alto nivel (esta vista) depende de la abstracción (ReporteExporter),
    no de la implementación concreta (CSVExporter).
    """
    pedidos = Pedido.objects.all().order_by('-fechaPedido')
    
    # Inyectar la dependencia concreta (CSVExporter)
    csv_exporter = CSVExporter()
    servicio = ReporteService(csv_exporter)
    
    # Generar el reporte
    return servicio.generar_reporte(pedidos)


@admin_required
def exportar_pedidos_pdf(request):
    """
    Exporta pedidos a PDF utilizando inversión de dependencias.
    Podemos intercambiar fácilmente entre CSV y PDF sin modificar la lógica.
    """
    pedidos = Pedido.objects.all().order_by('-fechaPedido')
    
    # Inyectar la dependencia concreta (PDFExporter)
    pdf_exporter = PDFExporter()
    servicio = ReporteService(pdf_exporter)
    
    # Generar el reporte
    return servicio.generar_reporte(pedidos)