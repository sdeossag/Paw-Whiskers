from django.utils.translation import gettext as _
from django.shortcuts import render
from productos.models import Producto  

def home(request):
    # Traer solo 3 productos (ejemplo: los más recientes)
    productos = Producto.objects.all()[:3]
    return render(request, 'tienda/home.html', {'productos': productos})

def productos(request):
    # Traer todos los productos
    productos = Producto.objects.all()
    return render(request, 'tienda/productos.html', {'productos': productos})