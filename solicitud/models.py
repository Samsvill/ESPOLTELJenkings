from django.db import models
from datetime import datetime
from django.db import models


# Create your models here.
class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=18)  #este se hace automatico
    nombre = models.CharField(max_length=200)
    tema = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    usuario_creacion = models.ForeignKey('user.UserProfile', related_name='solicitudes', on_delete=models.CASCADE)
    estado = models.ForeignKey('Estado', related_name='solicitudes', on_delete=models.CASCADE)
    proyecto = models.ForeignKey('proyecto.Proyecto', related_name='solicitudes', on_delete=models.CASCADE)
    cotizacion_aceptada = models.ForeignKey('Cotizacion', related_name='solicitudes', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - creado el {self.fecha_creacion}"

    def save(self, *args, **kwargs):
        self.codigo = self.generate_codigo(self.proyecto.nombre, self.proyecto)
        print(f"Generando código: {self.codigo}")  # Log del código generado
        super().save(*args, **kwargs)

    def generate_codigo(self, nombre, proyecto):
        # Formato: "NOMBR-AAAAMMDD-000"
        nombre_str = nombre[:3].upper() # usa las primeras tres letras del nombre
        fecha_str = datetime.now().strftime('%Y-%m-%d') # formato de la fecha: AAAAMMDD
        secuencia = self.get_secuencia(proyecto)
        codigo = f"{nombre_str}-{fecha_str}-{secuencia:03d}"
        return codigo

    def get_secuencia(self, proyecto):
        return Solicitud.objects.filter(proyecto=proyecto).count() + 1
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

class ItemSolicitud(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('proyecto.BudgetItem', related_name='items', on_delete=models.CASCADE)
    solicitud = models.ForeignKey('Solicitud', related_name='items', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} {self.unidad}"
    
    class Meta:
        verbose_name = "Item solicitud"
        verbose_name_plural = "Items solicitud"

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.mensaje}"
    
class Cotizacion(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey('Solicitud', related_name='cotizacion', on_delete=models.CASCADE)
    proveedor = models.CharField(max_length=100, null=True, blank=True, default=None)
    no_coti = models.SmallIntegerField(default=None, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    url_coti = models.URLField(null=True, blank=True, default=None)
    fecha_coti = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.no_coti} - {self.monto} - {self.proveedor}"
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"

class Formulario(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey('Solicitud', related_name='formulario', on_delete=models.CASCADE)
    cedula_ruc = models.CharField(max_length=13)
    tipo_compra = models.CharField(max_length=100, null=True, blank=True, default=None)
    no_compra = models.CharField(max_length=100, null=True, blank=True, default=None)
    url_compra = models.URLField(null=True, blank=True, default=None)

    tipo_acuerdo = models.CharField(max_length=100, null=True, blank=True, default=None)
    forma_pago = models.CharField(max_length=100, null=True, blank=True, default=None)
    tipo_pago = models.CharField(max_length=100, null=True, blank=True, default=None)
    tiempo = models.SmallIntegerField(null=True, blank=True, default=None)
    url_certi_banco = models.URLField(null=True, blank=True, default=None)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)

    nombre_banco = models.CharField(max_length=100, null=True, blank=True, default=None)
    tipo_cuenta = models.CharField(max_length=100, null=True, blank=True, default=None)
    numero_cuenta = models.CharField(max_length=100, null=True, blank=True, default=None)
    nombre_cuenta = models.CharField(max_length=100, null=True, blank=True, default=None)
    correo = models.EmailField(null=True, blank=True, default=None)
    def __str__(self):
        return f"{self.solicitud.codigo} - {self.cedula_ruc}"
    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"

class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey('Solicitud', related_name='factura', on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=5)
    comentario = models.CharField(max_length=200, null=True, blank=True, default=None)
    
    def __str__(self):
        return f"{self.no_factura} - {self.monto}"
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
