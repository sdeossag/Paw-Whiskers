from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Producto
from .forms import ProductoForm
import pandas as pd
from django.core.paginator import Paginator

# 🔓 Vista para todos (clientes y admin)
def listar_productos(request):
    productos = Producto.objects.filter(activo=True).order_by("id")

    # 🔍 Filtros
    query = request.GET.get(_("q"))  # nombre
    categoria = request.GET.get(_("categoria"))
    precio_min = request.GET.get(_("precio_min"))
    precio_max = request.GET.get(_("precio_max"))

    if query:
        productos = productos.filter(nombre__icontains=query)

    if categoria:
        productos = productos.filter(clasificacion__icontains=categoria)

    if precio_min:
        productos = productos.filter(precio__gte=precio_min)

    if precio_max:
        productos = productos.filter(precio__lte=precio_max)

    # Paginación (8 productos por página)
    paginator = Paginator(productos, 8)
    page_number = request.GET.get(_("page"))
    productos_page = paginator.get_page(page_number)

    return render(
        request,
        _("productos/productos.html"),
        {
            _("productos"): productos_page,
            "categorias": Producto.objects.values_list("clasificacion", flat=True).distinct()
        }
    )


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    return render(request, "productos/detalle_producto.html", {"producto": producto})


# 🔒 Solo staff puede subir Excel
def agregar_productos_excel(request):
    if not request.user.is_staff:
        messages.error(request, _("No tienes permisos para subir productos."))
        return redirect("home")

    if request.method == _("POST") and request.FILES.get(_("archivo_excel")):
        excel_file = request.FILES[_("archivo_excel")]

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            messages.error(request, f"Error al leer el Excel: {e}")
            return redirect("home")

        for _, row in df.iterrows():
            producto = Producto(
                nombre=row[_("nombre")],
                descripcion=row.get(_("descripcion"), ""),
                clasificacion=row.get(_("clasificacion"), ""),
                precio=row.get(_("precio"), 0),
                cantidadDisp=row.get(_("cantidadDisp"), 0),
            )
            if _("imagen") in row and pd.notna(row[_("imagen")]):
                producto.imagen = row[_("imagen")]
            producto.save()

        messages.success(request, _("Productos agregados exitosamente desde Excel."))
        return redirect("listar_productos")

    return render(request, "productos/subir_productos.html")


# ✅ Decorador para solo superusuarios
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


# 🔑 Vistas de administración (usan el MISMO template con condicionales)
@admin_required
def crear_producto(request):
    if request.method == _("POST"):
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Producto creado con éxito ✅"))
            return redirect("listar_productos")
    else:
        form = ProductoForm()

    return render(request, "productos/crear_producto.html", {"form": form})


@admin_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == _("POST"):
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, _("Producto actualizado con éxito ✏️"))
            return redirect("listar_productos")
    else:
        form = ProductoForm(instance=producto)
    return redirect("listar_productos")



@admin_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == _("POST"):
        producto.activo = False  # ✅ RF3: no borramos, solo desactivamos
        producto.save()
        messages.success(request, _("Producto eliminado (oculto al cliente) 🗑️"))
        return redirect("listar_productos")
    return redirect("listar_productos")

@admin_required
def restablecer_stock(request):
    if request.method == _("POST"):
        # Restablecer el stock de todos los productos a un valor por defecto, por ejemplo 20
        Producto.objects.all().update(cantidadDisp=20)
        messages.success(request, _("El stock de todos los productos ha sido restablecido a 20."))
    return redirect("listar_productos")
