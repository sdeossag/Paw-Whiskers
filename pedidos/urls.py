from django.urls import path
from . import views

urlpatterns = [
    path('', views.realizar_pedido, name="realizar_pedido"),
]
