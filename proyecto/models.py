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
    nombre = models.CharField(max_length=200, unique=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    project_budget = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - creado el {self.fecha_creacion}"

    class Meta:
        ordering = ['-fecha_creacion']

