from rest_framework import serializers
from .models import Proyecto, BudgetItem

class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem
        fields = ['id', 'recurso', 'categoria', 'cantidad', 'valor', 'presupuesto', 'proyecto']

    def create(self, validated_data):
        return BudgetItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.recurso = validated_data.get('recurso', instance.recurso)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.valor = validated_data.get('valor', instance.valor)
        instance.presupuesto = validated_data.get('presupuesto', instance.presupuesto)
        instance.proyecto = validated_data.get('proyecto', instance.proyecto)
        instance.save()
        return instance

class ProyectoSerializer(serializers.ModelSerializer):
    budget_items = BudgetItemSerializer(many=True, required=False)

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'fecha_creacion', 'usuario_creacion', 'project_budget', 'budget_items']
        read_only_fields = ['id', 'fecha_creacion']

    def create(self, validated_data):
        budget_items_data = validated_data.pop('budget_items', [])
        proyecto = Proyecto.objects.create(**validated_data)
        for item_data in budget_items_data:
            BudgetItem.objects.create(proyecto=proyecto, **item_data)
        return proyecto

    def update(self, instance, validated_data):
        budget_items_data = validated_data.pop('budget_items', [])
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.project_budget = validated_data.get('project_budget', instance.project_budget)
        instance.save()

        if budget_items_data is not None:
            for item_data in budget_items_data:
                item_id = item_data.get('id')
                if item_id is None:
                    BudgetItem.objects.create(proyecto=instance, **item_data)
                else:
                    item = BudgetItem.objects.get(id=item_id, proyecto=instance)
                    item.recurso = item_data.get('recurso', item.recurso)
                    item.categoria = item_data.get('categoria', item.categoria)
                    item.cantidad = item_data.get('cantidad', item.cantidad)
                    item.valor = item_data.get('valor', item.valor)
                    item.presupuesto = item_data.get('presupuesto', item.presupuesto)
                    item.save()
        return instance

