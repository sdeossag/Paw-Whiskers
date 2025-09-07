from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Administrador

@receiver(post_save, sender=User)
def crear_perfil_admin(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Administrador.objects.create(user=instance)
