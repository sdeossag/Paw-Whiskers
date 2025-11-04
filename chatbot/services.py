from django.utils.translation import gettext as _
# chatbot/services.py
from productos.models import Producto

def get_context_data(limit=10):
    """
    Retorna información de los productos activos en la base de datos,
    lista para que el LLM la use en sus respuestas.
    """
    productos = Producto.objects.filter(activo=True)[:limit]
    productos_list = [
        {
            _("nombre"): p.nombre,
            _("clasificacion"): p.clasificacion,
            _("precio"): float(p.precio),
            _("cantidadDisp"): p.cantidadDisp,
        }
        for p in productos
    ]
    return {"productos": productos_list}