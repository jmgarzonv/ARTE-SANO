from django import forms
from .models import Producto, Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class RegisterForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']
        labels = {
            'titulo': _('Título'),
            'descripcion': _('Descripción'),
            'precio': _('Precio'),
            'stock': _('Stock'),
            'categoria': _('Categoría'),
            'imagen': _('Imagen'),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Usuario"), max_length=150)
    password = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput)
