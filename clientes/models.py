from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idAdministrador = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Admin: {self.user.username}"

class CuentaCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccionPedido = models.CharField(max_length=200)
    metodoPago = models.CharField(max_length=50)

    def __str__(self):
        return f"Cliente: {self.user.username}"
