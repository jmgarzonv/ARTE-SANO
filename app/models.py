from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    artesano = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.artesano.username if self.artesano else 'Sin Artesano'}"

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username} - {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.cantidad} x {self.producto.titulo} (Pedido {self.pedido.id})'
    
class Carrito(models.Model):
    session_id = models.CharField(max_length=255, unique=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio