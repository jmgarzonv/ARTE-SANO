# app/services/order_service.py
from typing import Iterable, Optional
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import get_user_model
from ..models import Pedido, DetallePedido, CarritoItem
from .payment import PaymentMethod

User = get_user_model()

class OrderService:
    def __init__(self, payment_processor: PaymentMethod, **payment_kwargs):
        self.payment_processor = payment_processor
        self.payment_kwargs = payment_kwargs

    @transaction.atomic
    def place_order(
        self,
        usuario: Optional[User],
        items: Iterable[CarritoItem]
    ) -> Optional[Pedido]:
        """
        Procesa un pedido completo:
          1) Verifica stock de todos los ítems.
          2) Calcula total.
          3) Intenta el pago a través de self.payment_processor.
          4) Crea el Pedido y sus DetallePedido.
        Retorna el Pedido si todo fue OK, o None si el pago falló.
        """
        # 1) Verificar stock
        for item in items:
            if item.producto.stock < item.cantidad:
                # No hay stock suficiente, abortamos
                return None

        # 2) Calcular total
        total: Decimal = sum(item.subtotal() for item in items)

        # 3) Intentar pagar
        if not self.payment_processor.pay(usuario, total, **self.payment_kwargs):
            return None

        # 4) Crear pedido y detalles dentro de la transacción
        pedido = Pedido.objects.create(usuario=usuario, total=total)
        for item in items:
            producto = item.producto
            cantidad = item.cantidad

            # Descontar stock
            producto.stock -= cantidad
            producto.save()

            # Crear detalle
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )

        return pedido
