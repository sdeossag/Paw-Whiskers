from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from clientes.models import CuentaCliente
from productos.models import Producto
from carrito.models import Carrito, CarritoItem
from django.core.files.uploadedfile import SimpleUploadedFile


class CarritoCalculosTest(TestCase):
    """Prueba unitaria para verificar los cálculos del carrito"""
    
    def setUp(self):
        """Configuración inicial: crear usuario, cliente, productos y carrito"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Crear cuenta de cliente con los campos correctos
        self.cliente = CuentaCliente.objects.create(
            user=self.user,
            direccionPedido='Calle 123 #45-67',
            metodoPago='Tarjeta de Crédito'
        )
        
        # Crear imagen dummy para los productos
        imagen_dummy = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        # Crear productos con los campos correctos
        self.producto1 = Producto.objects.create(
            nombre='Laptop',
            descripcion='Laptop de alta gama',
            clasificacion='Electrónica',
            precio=Decimal('1000.00'),
            imagen=imagen_dummy,
            cantidadDisp=10,
            activo=True
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Mouse',
            descripcion='Mouse inalámbrico',
            clasificacion='Accesorios',
            precio=Decimal('50.00'),
            imagen=imagen_dummy,
            cantidadDisp=20,
            activo=True
        )
        
        # Crear carrito y agregar items
        self.carrito = Carrito.objects.create(cliente=self.cliente)
        
        CarritoItem.objects.create(
            carrito=self.carrito,
            producto=self.producto1,
            cantidad=2
        )
        
        CarritoItem.objects.create(
            carrito=self.carrito,
            producto=self.producto2,
            cantidad=3
        )
    
    def test_calculo_total_carrito(self):
        """
        Prueba que el cálculo del total del carrito sea correcto
        Total = (1000 * 2) + (50 * 3) = 2150
        Impuestos = 2150 * 0.19 = 408.50
        Total con impuestos = 2150 + 408.50 = 2558.50
        """
        # Verificar subtotal
        subtotal_esperado = Decimal('2150.00')
        self.assertEqual(self.carrito.subtotal_carrito, subtotal_esperado)
        
        # Verificar impuestos (19%)
        impuestos_esperados = Decimal('408.50')
        self.assertEqual(self.carrito.impuestos, impuestos_esperados)
        
        # Verificar total
        total_esperado = Decimal('2558.50')
        self.assertEqual(self.carrito.total_carrito, total_esperado)
        
        print(f"✓ Subtotal: ${self.carrito.subtotal_carrito}")
        print(f"✓ Impuestos: ${self.carrito.impuestos}")
        print(f"✓ Total: ${self.carrito.total_carrito}")