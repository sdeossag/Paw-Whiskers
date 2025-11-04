from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedidos'
    verbose_name = _("Pedidos")
