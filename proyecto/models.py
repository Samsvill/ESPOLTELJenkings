from django.db import models
from datetime import datetime

class BudgetItem(models.Model):
    recurso = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    valor = models.FloatField()
    presupuesto = models.FloatField(default=float(0))
    proyecto = models.ForeignKey('Proyecto', related_name='budget_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recurso} - {self.categoria}"


class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, default="Nuevo Proyecto")
    fecha_creacion = models.DateField(auto_now_add=True)
    project_budget = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - creado el {self.fecha_creacion}"

    class Meta:
        ordering = ['-fecha_creacion']

class ItemSolicitud(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('BudgetItem', related_name='items', on_delete=models.CASCADE)
    solicitud = models.ForeignKey('solicitud.Solicitud', related_name='items', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} {self.unidad}"
    
    class Meta:
        verbose_name = "Item solicitud"
        verbose_name_plural = "Items solicitud"