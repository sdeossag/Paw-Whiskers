from django.contrib import admin
from .models import Administrador, CuentaCliente

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ("user", "idAdministrador")
    search_fields = ("user__username", "idAdministrador")

@admin.register(CuentaCliente)
class CuentaClienteAdmin(admin.ModelAdmin):
    list_display = ("user", "direccionPedido", "metodoPago")
    search_fields = ("user__username", "direccionPedido")
    list_filter = ("metodoPago",)
