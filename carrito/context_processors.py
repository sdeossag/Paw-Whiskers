from django.utils.translation import gettext as _
from .models import Carrito, CuentaCliente

def carrito_context(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            cliente = CuentaCliente.objects.get(user=request.user)
            carrito, _ = Carrito.objects.get_or_create(cliente=cliente)
            return {'carrito_context': carrito}
        except CuentaCliente.DoesNotExist:
            return {'carrito_context': None}
    return {'carrito_context': None}