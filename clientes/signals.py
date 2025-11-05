from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Administrador, CuentaCliente

@receiver(post_save, sender=User)
def crear_perfiles(sender, instance, created, **kwargs):
    if created:
        # Todos los usuarios obtienen una cuenta de cliente para poder usar la tienda
        CuentaCliente.objects.create(user=instance)

        # Los superusuarios obtienen ADEMÁS un perfil de administrador
        if instance.is_superuser:
            Administrador.objects.create(user=instance)
