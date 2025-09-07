from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "clasificacion", "precio", "cantidadDisp", "activo")
    list_filter = ("clasificacion", "activo")
    search_fields = ("nombre", "descripcion")
    list_editable = ("precio", "cantidadDisp", "activo")  # editar en línea desde la lista
