from django.urls import path
from .views import lista_productos, crear_producto, eliminar_producto

urlpatterns = [
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/nuevo/', crear_producto, name='crear_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
]
