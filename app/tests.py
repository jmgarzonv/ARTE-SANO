from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Producto, Categoria
from django.contrib.auth.models import User

class ProductoTests(TestCase):
    def test_crear_producto(self):
        categoria = Categoria.objects.create(nombre="Textiles")
        producto = Producto.objects.create(
            titulo="Bufanda",
            descripcion="Hecha a mano",
            precio=25000,
            stock=10,
            categoria=categoria
        )
        self.assertEqual(producto.titulo, "Bufanda")
        self.assertEqual(producto.stock, 10)


from .models import Carrito, CarritoItem

class CarritoTests(TestCase):
    def test_agregar_al_carrito(self):
        categoria = Categoria.objects.create(nombre="Cerámica")
        producto = Producto.objects.create(
            titulo="Vasija",
            descripcion="Decorativa",
            precio=50000,
            stock=5,
            categoria=categoria
        )
        carrito = Carrito.objects.create(session_id="testsession123")
        item = CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=2)

        self.assertEqual(item.subtotal(), 100000)
