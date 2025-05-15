from .views import clima_medellin

def clima_context(request):
    return {
        'clima': clima_medellin()
    }
