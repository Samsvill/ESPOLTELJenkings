from django.contrib import admin
from .models import Solicitud, Estado, Cotizacion, Formulario
# Register your models here.
admin.site.register(Solicitud)
admin.site.register(Estado)
admin.site.register(Cotizacion)
admin.site.register(Formulario)