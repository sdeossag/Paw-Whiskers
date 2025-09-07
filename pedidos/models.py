from django.db import models
from clientes.models import CuentaCliente

class Pedido(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    fechaPedido = models.DateField(auto_now_add=True)
    totalPedido = models.DecimalField(max_digits=10, decimal_places=2)
    direccionPedido = models.CharField(max_length=200)

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.user.username}"

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pagos")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    metodoPago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago {self.cantidad} para Pedido #{self.pedido.id}"
