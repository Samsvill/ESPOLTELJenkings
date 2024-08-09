from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, BudgetItem
from solicitud.models import Solicitud
from .serializers import ProyectoSerializer, BudgetItemSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

class ProyectoListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            proyectos = Proyecto.objects.all()
            if proyectos.exists():
                serializer = ProyectoSerializer(proyectos, many=True)
                response_data = {
                    "status": "success",
                    "message": "Proyectos devueltos con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay proyectos creados",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ProyectoSerializer(data=request.data)
            if serializer.is_valid():
                proyecto = serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Proyecto creado exitosamente",
                    "data": {
                        "id": proyecto.id
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear el proyecto",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear el proyecto",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, instance, validated_data):
        budget_items_data = validated_data.pop('budget_items', None)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.project_budget = validated_data.get('project_budget', instance.project_budget)
        instance.save()

        if budget_items_data is not None:
            for item_data in budget_items_data:
                item_id = item_data.get('id')
                if item_id:
                    budget_item = BudgetItem.objects.get(id=item_id, proyecto=instance)
                    budget_item.recurso = item_data.get('recurso', budget_item.recurso)
                    budget_item.categoria = item_data.get('categoria', budget_item.categoria)
                    budget_item.cantidad = item_data.get('cantidad', budget_item.cantidad)
                    budget_item.valor = item_data.get('valor', budget_item.valor)
                    budget_item.presupuesto = item_data.get('presupuesto', budget_item.presupuesto)
                    budget_item.save()
                else:
                    BudgetItem.objects.create(proyecto=instance, **item_data)

        return instance   
        
class BudgetItemCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    #get de los items de un proyecto
    def get(self, request, proyecto_id):
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
            items = BudgetItem.objects.filter(proyecto=proyecto)
            if items.exists():
                serializer = BudgetItemSerializer(items, many=True)
                response_data = {
                    "status": "success",
                    "message": "Items devueltos con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay items creados",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {proyecto_id}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, proyecto_id):
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {proyecto_id}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            items_data = request.data.get('budget_items', [])
            errors = []
            for item_data in items_data:
                item_data['proyecto'] = proyecto_id
                serializer = BudgetItemSerializer(data=item_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
            
            if errors:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear uno o más items",
                    "errors": errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_data = {
                    "status": "success",
                    "message": "Items creados exitosamente para el proyecto",
                    "data": {
                        "proyecto_id": proyecto_id
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear los items",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProyectoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

#para un futuro detail del item de un proyecto, por ahora muestra todos
class BudgetItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BudgetItem.objects.all()
    serializer_class = BudgetItemSerializer

#GET y POST de los items de una solicitud por id
