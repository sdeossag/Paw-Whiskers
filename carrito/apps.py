from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CarritoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carrito'
    verbose_name = _("Carrito de Compras")
