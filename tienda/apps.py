from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TiendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tienda'
    verbose_name = _("Tienda")
