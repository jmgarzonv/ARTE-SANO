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
