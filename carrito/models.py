from django.db import models
from clientes.models import CuentaCliente
from productos.models import Producto
import decimal

class Carrito(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoItem")

    def __str__(self):
        return f"Carrito de {self.cliente.user.username}"

    @property
    def subtotal_carrito(self):
        return sum(item.subtotal for item in self.carritoitem_set.all())

    @property
    def impuestos(self):
        return self.subtotal_carrito * decimal.Decimal('0.19')

    @property
    def total_carrito(self):
        return self.subtotal_carrito + self.impuestos

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

class Favorito(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return f"Favoritos de {self.cliente.user.username}"
