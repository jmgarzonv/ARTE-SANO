# app/services/payment.py
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional
from django.contrib.auth import get_user_model
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.storage import default_storage
from django.conf import settings

User = get_user_model()

class PaymentError(Exception):
    pass

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, usuario: Optional[User], monto: Decimal, **kwargs) -> bool:
        ...

class CheckPayment(PaymentMethod):
    """
    Simula un pago con cheque y genera un PDF en MEDIA_ROOT/cheques/
    guardado bajo un nombre único.
    """
    def pay(self, usuario: Optional[User], monto: Decimal, **kwargs) -> bool:
        check_number = kwargs.get('check_number', 'sin-numero')

        # 1) Creamos un buffer en memoria
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # 2) Dibujamos texto en el PDF
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, 800, "Cheque de pago - ARTE SANO")
        p.setFont("Helvetica", 12)
        p.drawString(50, 770, f"Numero de cheque: {check_number}")
        p.drawString(50, 750, f"Monto: ${monto}")
        nombre = usuario.username if usuario else "Invitado"
        p.drawString(50, 730, f"Pagador: {nombre}")
        p.drawString(50, 710, f"Email: {usuario.email if usuario else '---'}")

        p.showPage()
        p.save()

        # 3) Guardamos el buffer en MEDIA_ROOT/cheques/cheque_<ts>.pdf
        buffer.seek(0)
        import time
        timestamp = int(time.time())
        filename = f"cheques/cheque_{timestamp}.pdf"
        full_path = default_storage.save(filename, buffer)

        # Guardamos la ruta para que la vista lo recupere
        self.receipt_path = default_storage.url(full_path)
        return True

class BalancePayment:
    def pay(self, user, total, **kwargs):
        # Permite el pago sin validar saldo
        return True


