from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from clientes.models import CuentaCliente
from productos.models import Producto
from carrito.models import Carrito, CarritoItem
from django.core.files.uploadedfile import SimpleUploadedFile


class CarritoCalculosTest(TestCase):
    """Prueba unitaria para verificar los cálculos del carrito con productos reales"""
    
    def setUp(self):
        """Configuración inicial: crear usuario, cliente y productos"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Crear cuenta de cliente
        self.cliente = CuentaCliente.objects.create(
            user=self.user,
            direccionPedido='Calle 123 #45-67',
            metodoPago='Tarjeta de Crédito'
        )
        
        # Crear imagen dummy
        imagen_dummy = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        # Crear productos de prueba que simulan productos reales
        self.producto1 = Producto.objects.create(
            nombre='Collar para Perro Premium',
            descripcion='Collar ajustable de cuero genuino',
            clasificacion='Accesorios',
            precio=Decimal('45.99'),
            imagen=imagen_dummy,
            cantidadDisp=25,
            activo=True
        )
        
        self.producto2 = Producto.objects.create(
            nombre='Juguete Interactivo para Gato',
            descripcion='Ratón con sonido y movimiento',
            clasificacion='Juguetes',
            precio=Decimal('18.50'),
            imagen=imagen_dummy,
            cantidadDisp=50,
            activo=True
        )
    
    def test_calculo_total_carrito_con_productos_reales(self):
        """
        Prueba que el cálculo del total del carrito sea correcto
        usando productos que simulan el inventario real de la tienda
        """
        print("\n" + "="*60)
        print("PRUEBA: CÁLCULO DEL CARRITO DE COMPRAS")
        print("="*60)
        
        # Crear carrito
        carrito = Carrito.objects.create(cliente=self.cliente)
        print(f"\n✓ Carrito creado para: {self.cliente.user.username}")
        
        # Agregar items al carrito con cantidades específicas
        cantidad1 = 2
        cantidad2 = 3
        
        item1 = CarritoItem.objects.create(
            carrito=carrito,
            producto=self.producto1,
            cantidad=cantidad1
        )
        
        item2 = CarritoItem.objects.create(
            carrito=carrito,
            producto=self.producto2,
            cantidad=cantidad2
        )
        
        print(f"\n📦 PRODUCTOS AGREGADOS AL CARRITO:")
        print(f"  1. {self.producto1.nombre}")
        print(f"     Precio unitario: ${self.producto1.precio}")
        print(f"     Cantidad: {cantidad1}")
        print(f"     Subtotal: ${item1.subtotal}")
        
        print(f"\n  2. {self.producto2.nombre}")
        print(f"     Precio unitario: ${self.producto2.precio}")
        print(f"     Cantidad: {cantidad2}")
        print(f"     Subtotal: ${item2.subtotal}")
        
        # Calcular valores esperados manualmente
        subtotal_esperado = (self.producto1.precio * cantidad1) + (self.producto2.precio * cantidad2)
        impuestos_esperados = subtotal_esperado * Decimal('0.19')
        total_esperado = subtotal_esperado + impuestos_esperados
        
        print(f"\n💰 RESUMEN FINANCIERO:")
        print(f"  Subtotal:           ${subtotal_esperado}")
        print(f"  Impuestos (19%):    ${impuestos_esperados}")
        print(f"  TOTAL A PAGAR:      ${total_esperado}")
        
        # Verificar subtotal
        self.assertEqual(carrito.subtotal_carrito, subtotal_esperado)
        print(f"\n✓ Subtotal verificado correctamente")
        
        # Verificar impuestos (19%)
        self.assertEqual(carrito.impuestos, impuestos_esperados)
        print(f"✓ Impuestos calculados correctamente")
        
        # Verificar total
        self.assertEqual(carrito.total_carrito, total_esperado)
        print(f"✓ Total del carrito correcto")
        
        print("\n" + "="*60)
        print("✅ PRUEBA EXITOSA: Todos los cálculos son correctos")
        print("="*60 + "\n")