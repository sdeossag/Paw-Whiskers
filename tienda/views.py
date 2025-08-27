from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Producto, Carrito, CarritoItem, Pedido, CuentaCliente
from django.contrib.auth.models import User
import pandas as pd

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "tienda/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)  # inicia sesión inmediatamente
        messages.success(request, f"Bienvenido {username}, tu cuenta fue creada 🎉")
        return redirect("home")

    return render(request, "tienda/register.html")


def listar_productos(request):
    productos = Producto.objects.all()
    query = request.GET.get("q")
    if query:
        productos = productos.filter(nombre__icontains=query)  # búsqueda
    return render(request, "tienda/productos.html", {"productos": productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "tienda/detalle_producto.html", {"producto": producto})


@login_required
def ver_carrito(request):
    cliente = get_object_or_404(CuentaCliente, user=request.user)
    carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
    items = carrito.carritoitem_set.all()
    return render(request, "tienda/carrito.html", {"carrito": carrito, "items": items})

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
        # Vaciar carrito
        carrito.carritoitem_set.all().delete()
        carrito.totalCarrito = 0
        carrito.save()
        messages.success(request, "Pedido realizado con éxito")
        return redirect("listar_productos")

    return render(request, "tienda/pedido.html", {"carrito": carrito})


def home(request):
    productos = Producto.objects.all().order_by('?')[:3]  # random 3 productos
    return render(request, "tienda/home.html", {"productos": productos})


@login_required
def agregar_productos_excel(request):
    # Solo administradores deberían acceder
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para subir productos.")
        return redirect("home")

    if request.method == "POST" and request.FILES.get("archivo_excel"):
        excel_file = request.FILES["archivo_excel"]

        try:
            df = pd.read_excel(excel_file)  # leer Excel
        except Exception as e:
            messages.error(request, f"Error al leer el Excel: {e}")
            return redirect("home")

        # Columnas esperadas: nombre, descripcion, clasificacion, precio, cantidadDisp, imagen (opcional)
        for _, row in df.iterrows():
            producto = Producto(
                nombre=row["nombre"],
                descripcion=row.get("descripcion", ""),
                clasificacion=row.get("clasificacion", ""),
                precio=row.get("precio", 0),
                cantidadDisp=row.get("cantidadDisp", 0),
            )
            # Si hay una columna imagen con URL o path
            if "imagen" in row and pd.notna(row["imagen"]):
                producto.imagen = row["imagen"]
            producto.save()

        messages.success(request, "Productos agregados exitosamente desde Excel.")
        return redirect("listar_productos")

    return render(request, "tienda/subir_productos.html")