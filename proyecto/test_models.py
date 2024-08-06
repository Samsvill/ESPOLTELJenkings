from django.test import TestCase

# Create your tests here.
from proyecto.models import Proyecto, BudgetItem
from datetime import datetime

#Solo se testean los modelos, no se testean las vistas
class ProyectoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Proyecto.objects.create(nombre='Proyecto de Prueba', project_budget=100000)

    def test_nombre_label(self):
        proyecto = Proyecto.objects.get(id=1)
        field_label = proyecto._meta.get_field('nombre').verbose_name
        self.assertEqual(field_label, 'nombre')

    def test_fecha_creacion_label(self):
        proyecto = Proyecto.objects.get(id=1)
        field_label = proyecto._meta.get_field('fecha_creacion').verbose_name
        self.assertEqual(field_label, 'fecha creacion')

    def test_project_budget_label(self):
        proyecto = Proyecto.objects.get(id=1)
        field_label = proyecto._meta.get_field('project_budget').verbose_name
        self.assertEqual(field_label, 'project budget')

    def test_nombre_max_length(self):
        proyecto = Proyecto.objects.get(id=1)
        max_length = proyecto._meta.get_field('nombre').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_nombre_fecha_creacion(self):
        proyecto = Proyecto.objects.get(id=1)
        expected_object_name = f'{proyecto.nombre} - creado el {proyecto.fecha_creacion}'
        self.assertEqual(str(proyecto), expected_object_name)

class BudgetItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        proyecto = Proyecto.objects.create(nombre='Proyecto de Prueba', project_budget=100000)
        BudgetItem.objects.create(recurso='Hormigon', categoria='Materiales', cantidad=10, valor=1000, proyecto=proyecto)

    def test_recurso_label(self):
        budget_item = BudgetItem.objects.get(id=1)
        field_label = budget_item._meta.get_field('recurso').verbose_name
        self.assertEqual(field_label, 'recurso')

    def test_categoria_label(self):
        budget_item = BudgetItem.objects.get(id=1)
        field_label = budget_item._meta.get_field('categoria').verbose_name
        self.assertEqual(field_label, 'categoria')

    def test_cantidad_label(self):
        budget_item = BudgetItem.objects.get(id=1)
        field_label = budget_item._meta.get_field('cantidad').verbose_name
        self.assertEqual(field_label, 'cantidad')

    def test_valor_label(self):
        budget_item = BudgetItem.objects.get(id=1)
        field_label = budget_item._meta.get_field('valor').verbose_name
        self.assertEqual(field_label, 'valor')

    def test_presupuesto_label(self):
        budget_item = BudgetItem.objects.get(id=1)
        field_label = budget_item._meta.get_field('presupuesto').verbose_name
        self.assertEqual(field_label, 'presupuesto')

    def test_proyecto_label(self):
        budget_item = BudgetItem.objects.get(id=1)
        field_label = budget_item._meta.get_field('proyecto').verbose_name
        self.assertEqual(field_label, 'proyecto')

    def test_recurso_max_length(self):
        budget_item = BudgetItem.objects.get(id=1)
        max_length = budget_item._meta.get_field('recurso').max_length
        self.assertEqual(max_length, 100)

    def test_categoria_max_length(self):
        budget_item = BudgetItem.objects.get(id=1)
        max_length = budget_item._meta.get_field('categoria').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_recurso_categoria(self):
        budget_item = BudgetItem.objects.get(id=1)
        expected_object_name = f'{budget_item.recurso} - {budget_item.categoria}'
        self.assertEqual(str(budget_item), expected_object_name)