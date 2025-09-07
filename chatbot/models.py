from django.db import models
from clientes.models import CuentaCliente

class ChatbotLog(models.Model):
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE)
    pregunta = models.TextField()
    respuesta = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chatbot log de {self.cliente.user.username} - {self.fecha}"
