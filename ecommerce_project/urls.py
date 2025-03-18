"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from app.views import home  # Importa la vista de la página de inicio
from django.conf.urls.static import static
from app.views import home  # Importa la vista de la página de inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Agrega esta línea para definir la página de inicio
    path('productos/', include('app.urls')),  # Asegúrate de que los productos están en un `include`
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)