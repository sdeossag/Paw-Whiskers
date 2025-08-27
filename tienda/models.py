from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idAdministrador = models.CharField(max_length=20, unique=True)

    def añadirProducto(self): ...
    def cancelarPedido(self): ...
    def retirarProducto(self): ...
    def editarProducto(self): ...

class CuentaCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccionPedido = models.CharField(max_length=200)
    metodoPago = models.CharField(max_length=50)

    def iniciarSesion(self): ...
    def registrarse(self): ...
    def cerrarSesion(self): ...
    def actualizarDatos(self): ...

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    clasificacion = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/")
    cantidadDisp = models.PositiveIntegerField()

    def buscar(self): ...
    def buscarFiltro(self): ...
    def restarCantidad(self): ...
    def añadirCantidad(self): ...

class Carrito(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoItem")
    totalCarrito = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Favorito(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)

class Pedido(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    fechaPedido = models.DateField(auto_now_add=True)
    totalPedido = models.DecimalField(max_digits=10, decimal_places=2)
    direccionPedido = models.CharField(max_length=200)

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pagos")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    metodoPago = models.CharField(max_length=50)
