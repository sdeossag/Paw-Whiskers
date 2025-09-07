from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    clasificacion = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/")
    cantidadDisp = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)  # 👈 agrega esto
    def __str__(self):
        return self.nombre
