from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from clientes.models import CuentaCliente
from pedidos.models import Pedido, Pago


class PedidoEstadoTest(TestCase):
    """Prueba unitaria para verificar la creación y estado de pedidos"""
    
    def setUp(self):
        """Configuración inicial: crear usuario, cliente y pedido"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='clientetest',
            email='cliente@test.com',
            password='pass123'
        )
        
        # Crear cuenta de cliente con los campos correctos
        self.cliente = CuentaCliente.objects.create(
            user=self.user,
            direccionPedido='Carrera 50 #30-20',
            metodoPago='Tarjeta de Débito'
        )
        
        # Crear pedido
        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            totalPedido=Decimal('500.00'),
            direccionPedido='Carrera 50 #30-20',
            estado='Pendiente'
        )
        
        # Crear pago para el pedido
        self.pago = Pago.objects.create(
            pedido=self.pedido,
            cantidad=Decimal('500.00'),
            metodoPago='Tarjeta de Débito'
        )
    
    def test_pedido_creacion_y_estado(self):
        """
        Prueba que un pedido se crea correctamente con estado 'Pendiente'
        y que el pago está asociado correctamente
        """
        # Verificar que el pedido se creó correctamente
        self.assertEqual(self.pedido.cliente, self.cliente)
        self.assertEqual(self.pedido.totalPedido, Decimal('500.00'))
        self.assertEqual(self.pedido.direccionPedido, 'Carrera 50 #30-20')
        
        # Verificar estado inicial
        self.assertEqual(self.pedido.estado, 'Pendiente')
        
        # Verificar que el pago está asociado al pedido
        self.assertEqual(self.pedido.pagos.count(), 1)
        self.assertEqual(self.pago.cantidad, Decimal('500.00'))
        self.assertEqual(self.pago.metodoPago, 'Tarjeta de Débito')
        
        print(f"✓ Pedido #{self.pedido.id} creado correctamente")
        print(f"✓ Estado: {self.pedido.estado}")
        print(f"✓ Total: ${self.pedido.totalPedido}")
        
        # Cambiar estado del pedido
        self.pedido.estado = 'Finalizado'
        self.pedido.save()
        
        # Verificar que el estado cambió
        pedido_actualizado = Pedido.objects.get(id=self.pedido.id)
        self.assertEqual(pedido_actualizado.estado, 'Finalizado')
        
        print(f"✓ Estado actualizado a: {pedido_actualizado.estado}")