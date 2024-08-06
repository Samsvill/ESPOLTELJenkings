from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, BudgetItem, ItemSolicitud
from solicitud.models import Solicitud
from .serializers import ProyectoSerializer, BudgetItemSerializer, ItemSolicitudSerializer
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
            items_data = request.data.get('items', [])
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
class ItemSolicitudListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk_s):
        try:
            items = ItemSolicitud.objects.filter(solicitud=pk_s)
            if items.exists():
                serializer = ItemSolicitudSerializer(items, many=True)
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
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            items_solicitud_data = request.data.get('items_solicitud', [])
            errors = []
            for item_data in items_solicitud_data:
                item_data['solicitud'] = pk_s
                serializer = ItemSolicitudSerializer(data=item_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
            
            if errors:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear uno o más items_solicitud",
                    "errors": errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_data = {
                    "status": "success",
                    "message": "Items_solicitud creados exitosamente para la solicitud",
                    "data": {
                        "solicitud_id": pk_s
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear los items_solicitud",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)