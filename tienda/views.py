from django.utils.translation import gettext as _
from django.shortcuts import render
from productos.models import Producto
import requests # Importar la librería requests

def home(request):
    # Traer solo 3 productos (ejemplo: los más recientes)
    productos = Producto.objects.all()[:3]
    return render(request, 'tienda/home.html', {'productos': productos})

def productos(request):
    # Traer todos los productos
    productos = Producto.objects.all()
    return render(request, 'tienda/productos.html', {'productos': productos})

# --- NUEVA VISTA PARA PRODUCTOS ALIADOS ---
def productos_aliados(request):
    # URL del servicio del Equipo 
    api_url = "http://98.89.217.213/api/recipes/"
    
    productos_data = []
    error_message = None

    try:
        response = requests.get(api_url)
        # Lanza una excepción si la respuesta tiene un código de error (4xx o 5xx)
        response.raise_for_status() 
        
        productos_data = response.json()

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión, timeouts, etc.
        error_message = f"Error al conectar con el servicio de productos aliados: {e}"
    except ValueError:
        # Manejar errores si la respuesta no es un JSON válido
        error_message = "Error: La respuesta del servicio no es un JSON válido."

    context = {
        'productos_aliados': productos_data,
        'error_message': error_message,
    }
    
    return render(request, 'tienda/productos_aliados.html', context)