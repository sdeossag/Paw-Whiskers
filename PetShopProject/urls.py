from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),
    path('productos/', include('productos.urls')),
    path('carrito/', include('carrito.urls')),
    path('pedido/', include('pedidos.urls')),
    path('clientes/', include('clientes.urls')),
    path("chatbot/", include("chatbot.urls")),

    # ✅ Agrega esta línea para habilitar set_language
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
