from django.contrib import admin
from .models import *
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType

admin.site.register(ContentType)
admin.site.register(Permission)

# Register your models here.
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Perfil)
admin.site.register(Producto)
admin.site.register(ProductoCategoria)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Paquete)
admin.site.register(PaqueteProducto)
