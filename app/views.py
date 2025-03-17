from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm

# Vista para listar productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

# Vista para agregar productos
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)

            # Solo asignar un usuario si está autenticado
            if request.user.is_authenticated:
                producto.artesano = request.user  
            else:
                producto.artesano = None  # Permitir productos sin usuario
            
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/crear_producto.html', {'form': form})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('lista_productos') 