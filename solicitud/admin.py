from django.contrib import admin
from .models import Solicitud, ItemSolicitud, Estado, Cotizacion, Formulario, Factura
# Register your models here.
admin.site.register(Solicitud)
admin.site.register(ItemSolicitud)
admin.site.register(Estado)
admin.site.register(Cotizacion)
admin.site.register(Formulario)
admin.site.register(Factura)