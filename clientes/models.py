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

class RegistroActividad(models.Model):
    TIPO_ACTIVIDAD_CHOICES = [
        ('CARRITO', 'Añadió al carrito'),
        ('FAVORITO', 'Añadió a favoritos'),
        ('PEDIDO', 'Pedido realizado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_actividad = models.CharField(max_length=20, choices=TIPO_ACTIVIDAD_CHOICES)
    detalles = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.get_tipo_actividad_display()} - {self.fecha.strftime("%Y-%m-%d %H:%M")}'

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ['-fecha']
