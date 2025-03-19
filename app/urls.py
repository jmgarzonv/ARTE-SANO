from django.urls import path
from .views import (
    lista_pedidos, lista_productos, crear_producto, eliminar_producto, comprar_producto,
    ver_carrito, agregar_al_carrito,finalizar_compra, eliminar_del_carrito  # Asegurar estas importaciones
)

urlpatterns = [
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('comprar/', comprar_producto, name='comprar_producto'),
    path('pedidos/', lista_pedidos, name='lista_pedidos'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/finalizar/', finalizar_compra, name='finalizar_compra'),  # Nueva ruta para comprar desde el carrito
]
