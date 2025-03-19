import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm
from django.views.decorators.csrf import csrf_exempt  # Asegurar esta importación
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from .models import Carrito, CarritoItem, Producto


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



def lista_pedidos(request):
    pedidos = Pedido.objects.all().prefetch_related('detalles')  # Muestra todos los pedidos
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})



def home(request):
    return render(request, 'index.html')  # Asegúrate de tener este template

@csrf_exempt
def comprar_producto(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                # Manejo de solicitudes JSON (API)
                data = json.loads(request.body)
                productos = data.get('productos', [])
            else:
                # Manejo de formularios HTML
                producto_id = request.POST.get('producto_id')
                cantidad = int(request.POST.get('cantidad', 1))
                productos = [{'producto_id': producto_id, 'cantidad': cantidad}]

            if not productos:
                return JsonResponse({'error': 'No se enviaron productos'}, status=400)

            pedido = Pedido.objects.create(total=0)
            total_pedido = 0

            for item in productos:
                producto_id = item.get('producto_id')
                cantidad = item.get('cantidad', 1)

                producto = get_object_or_404(Producto, id=producto_id)

                if producto.stock < cantidad:
                    return JsonResponse({'error': f'Stock insuficiente para {producto.titulo}'}, status=400)

                producto.stock -= cantidad
                producto.save()

                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                total_pedido += detalle.subtotal()

            pedido.total = total_pedido
            pedido.save()

            if request.content_type == 'application/json':
                return JsonResponse({'mensaje': 'Compra realizada con éxito', 'pedido_id': pedido.id})
            else:
                return redirect('lista_pedidos')  # Redirigir a la página de pedidos en HTML

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_carrito(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    carrito, created = Carrito.objects.get_or_create(session_id=session_id)
    return carrito

def agregar_al_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
        item.save()

    return JsonResponse({'mensaje': 'Producto agregado al carrito'})

def eliminar_del_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    CarritoItem.objects.filter(carrito=carrito, producto=producto).delete()
    
    return JsonResponse({'mensaje': 'Producto eliminado del carrito'})

def ver_carrito(request):
    carrito = obtener_carrito(request)
    items = carrito.items.all()
    
    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito, 'items': items})

def agregar_al_carrito(request, producto_id):
    carrito = obtener_carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito')  # Redirige al carrito después de agregar un producto

def finalizar_compra(request):
    carrito = obtener_carrito(request)
    items = carrito.items.all()

    if not items:
        return redirect('ver_carrito')

    pedido = Pedido.objects.create(total=0)
    total_pedido = 0

    for item in items:
        producto = item.producto
        cantidad = item.cantidad

        if producto.stock < cantidad:
            return JsonResponse({'error': f'Stock insuficiente para {producto.titulo}'}, status=400)

        # Reducir stock
        producto.stock -= cantidad
        producto.save()

        # Guardar detalle de pedido
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )

        total_pedido += detalle.subtotal()

    pedido.total = total_pedido
    pedido.save()

    # Vaciar el carrito después de la compra
    carrito.items.all().delete()

    return redirect('lista_pedidos')  # Redirigir a la lista de pedidos
