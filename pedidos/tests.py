from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from clientes.models import CuentaCliente
from productos.models import Producto
from pedidos.models import Pedido, Pago
from django.core.files.uploadedfile import SimpleUploadedFile


class PedidoEstadoTest(TestCase):
    """Prueba unitaria para verificar la creación y estado de pedidos con productos reales"""
    
    def setUp(self):
        """Configuración inicial: crear usuario, cliente y productos"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='clientetest',
            email='cliente@test.com',
            password='pass123'
        )
        
        # Crear cuenta de cliente
        self.cliente = CuentaCliente.objects.create(
            user=self.user,
            direccionPedido='Carrera 50 #30-20',
            metodoPago='Tarjeta de Débito'
        )
        
        # Crear imagen dummy
        imagen_dummy = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        # Crear productos de prueba que simulan productos reales
        self.producto1 = Producto.objects.create(
            nombre='Cama Ortopédica para Mascotas',
            descripcion='Cama cómoda con soporte lumbar',
            clasificacion='Muebles',
            precio=Decimal('89.99'),
            imagen=imagen_dummy,
            cantidadDisp=15,
            activo=True
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Alimento Premium para Gatos 5kg',
            descripcion='Alimento balanceado con salmón',
            clasificacion='Alimentos',
            precio=Decimal('34.50'),
            imagen=imagen_dummy,
            cantidadDisp=40,
            activo=True
        )
    
    def test_pedido_creacion_con_productos_reales(self):
        """
        Prueba que un pedido se crea correctamente con estado 'Pendiente'
        usando productos que simulan el inventario real
        """
        print("\n" + "="*60)
        print("PRUEBA: GESTIÓN DE PEDIDOS Y ESTADOS")
        print("="*60)
        
        # Calcular el total del pedido basado en productos reales
        cantidad1 = 1
        cantidad2 = 2
        
        print(f"\n📦 PRODUCTOS DEL PEDIDO:")
        print(f"  1. {self.producto1.nombre}")
        print(f"     Precio: ${self.producto1.precio} x {cantidad1} = ${self.producto1.precio * cantidad1}")
        
        print(f"\n  2. {self.producto2.nombre}")
        print(f"     Precio: ${self.producto2.precio} x {cantidad2} = ${self.producto2.precio * cantidad2}")
        
        subtotal = (self.producto1.precio * cantidad1) + (self.producto2.precio * cantidad2)
        impuestos = subtotal * Decimal('0.19')
        total_pedido = subtotal + impuestos
        
        print(f"\n💰 CÁLCULO DEL PEDIDO:")
        print(f"  Subtotal:        ${subtotal}")
        print(f"  Impuestos (19%): ${impuestos}")
        print(f"  TOTAL:           ${total_pedido}")
        
        # Crear pedido
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            totalPedido=total_pedido,
            direccionPedido=self.cliente.direccionPedido,
            estado='Pendiente'
        )
        
        print(f"\n✓ Pedido #{pedido.id} creado exitosamente")
        print(f"  Cliente: {self.cliente.user.username}")
        print(f"  Fecha: {pedido.fechaPedido}")
        print(f"  Dirección: {pedido.direccionPedido}")
        print(f"  Estado inicial: {pedido.estado}")
        
        # Crear pago para el pedido
        pago = Pago.objects.create(
            pedido=pedido,
            cantidad=total_pedido,
            metodoPago=self.cliente.metodoPago
        )
        
        print(f"\n💳 PAGO REGISTRADO:")
        print(f"  Método: {pago.metodoPago}")
        print(f"  Monto: ${pago.cantidad}")
        
        # Verificar que el pedido se creó correctamente
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertEqual(pedido.totalPedido, total_pedido)
        self.assertEqual(pedido.direccionPedido, self.cliente.direccionPedido)
        print(f"\n✓ Datos del pedido verificados correctamente")
        
        # Verificar estado inicial
        self.assertEqual(pedido.estado, 'Pendiente')
        print(f"✓ Estado inicial 'Pendiente' verificado")
        
        # Verificar que el pago está asociado al pedido
        self.assertEqual(pedido.pagos.count(), 1)
        self.assertEqual(pago.cantidad, total_pedido)
        self.assertEqual(pago.metodoPago, self.cliente.metodoPago)
        print(f"✓ Pago asociado correctamente al pedido")
        
        # Cambiar estado del pedido
        print(f"\n🔄 ACTUALIZANDO ESTADO DEL PEDIDO...")
        pedido.estado = 'Finalizado'
        pedido.save()
        
        # Verificar que el estado cambió
        pedido_actualizado = Pedido.objects.get(id=pedido.id)
        self.assertEqual(pedido_actualizado.estado, 'Finalizado')
        print(f"✓ Estado actualizado a: '{pedido_actualizado.estado}'")
        
        print("\n" + "="*60)
        print("✅ PRUEBA EXITOSA: Pedido creado y actualizado correctamente")
        print("="*60 + "\n")