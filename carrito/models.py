from django.db import models
from clientes.models import CuentaCliente
from productos.models import Producto

class Carrito(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoItem")

    def __str__(self):
        return f"Carrito de {self.cliente.user.username}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"

class Favorito(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return f"Favoritos de {self.cliente.user.username}"
