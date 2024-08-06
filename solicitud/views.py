from datetime import datetime

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Solicitud, Estado, Cotizacion, Formulario, Factura
from .serializers import SolicitudSerializer, CotizacionSerializer, FormularioSerializer, FacturaSerializer
from proyecto.models import Proyecto
from user.models import UserProfile


# Create your views here.
ERROR_MESSAGE = "Fallo en la consulta"

#crear una solicitud de un proyecto YA EXISTENTE y GET de todas las solicitudes
class SolicitudCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SolicitudSerializer
    def post(self, request, pk):
        try:
            proyecto = Proyecto.objects.get(id=pk)
            usuario = UserProfile.objects.get(user=request.user)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            request.data['proyecto'] = proyecto.id
            request.data['usuario_creacion'] = usuario.id
            serializer = SolicitudSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Solicitud creada exitosamente",
                    "data": {
                        "proyecto_id": pk,
                        "solicitud_id": serializer.data['id'],
                        "codigo": serializer.data['codigo']
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear la solicitud, error del serializer",
                    "errors": serializer.errors,
                    "serializer_data": serializer.data
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear la solicitud",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#GET de solicitudes por usuario loggeado
class SolicitudByUserAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudSerializer
    def get(self, request):
        solicitudes = Solicitud.objects.filter(usuario_creacion= UserProfile.objects.get(user=request.user))
        serializer = SolicitudSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#GET de todas las solicitudes
class SolicitudGetAllAPIView(generics.ListAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            solicitudes = Solicitud.objects.all()
            if solicitudes.exists():
                serializer = SolicitudSerializer(solicitudes, many=True)
                response_data = {
                    "status": "success",
                    "message": "Solicitudes devueltas con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay solicitudes creadas",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": ERROR_MESSAGE,
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET y PUT de una solicitud por id
class SolicitudDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            solicitud = Solicitud.objects.get(id=pk)
            serializer = SolicitudSerializer(solicitud)
            response_data = {
                "status": "success",
                "message": "Solicitud devuelta con éxito",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": ERROR_MESSAGE,
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            solicitud = Solicitud.objects.get(id=pk)
            coti_nueva = Cotizacion.objects.get(id=request.data['cotizacion_aceptada'])
            solicitud.cotizacion_aceptada = coti_nueva
            serializer = SolicitudSerializer(solicitud, data= request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Solicitud actualizada exitosamente",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo actualizar la solicitud, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo actualizar la solicitud",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# PUT del estado de una solicitud
class EstadoUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudSerializer

    def put(self, request, pk_p, pk_s, pk_e):
        try:
            solicitud = Solicitud.objects.get(id=pk_s, proyecto=pk_p)
            estado_nuevo = Estado.objects.get(id=pk_e)
            request.data['estado'] = estado_nuevo.id
            serializer = SolicitudSerializer(solicitud, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": f"Estado de la solicitud actualizado exitosamente a '{estado_nuevo.mensaje}'" 
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo actualizar el estado, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s} en el proyecto con id {pk_p}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Estado.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el estado con id {pk_e}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo actualizar el estado",
                "error": str(e),
                "request": request.data
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#GET de estado de una solicitud
class EstadoListAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudSerializer
    def get(self, request, pk_p, pk_s):
        try:
            solicitud = Solicitud.objects.get(proyecto=pk_p, id=pk_s)
            serializer = SolicitudSerializer(solicitud)
            response_data = {
                "status": "success",
                "message": "Estado devuelto con éxito",
                "data": {
                    "solicitud_id": pk_s,
                    "estado_id": serializer.data['estado'],
                    "estado": Estado.objects.get(id=serializer.data['estado']).mensaje,
                    "mensaje": Estado.objects.get(id=serializer.data['estado']).nombre,

                    
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s} en el proyecto con id {pk_p}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": ERROR_MESSAGE,
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#GET y POST de cotizaciones de una solicitud
class CotizacionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudSerializer
    def get(self, request, pk):
        try:
            solicitud = Solicitud.objects.get(id=pk)
            cotizaciones = Cotizacion.objects.filter(solicitud=solicitud)
            cotizaciones_data = []
            for cotizacion in cotizaciones:
                cotizacion_data = {
                    "id": cotizacion.id,
                    "solicitud_id": cotizacion.solicitud.id,
                    #"usuario_creacion": cotizacion.usuario_creacion.id,
                    "proveedor": cotizacion.proveedor,
                    "no_coti": cotizacion.no_coti,
                    "monto": str(cotizacion.monto),
                    "fecha_coti": cotizacion.fecha_coti.strftime("%d-%m-%Y") if cotizacion.fecha_coti is not None else None,
                    "file_coti": cotizacion.file_coti.url if cotizacion.file_coti else None
                }
                cotizaciones_data.append(cotizacion_data)
            response_data = {
                "status": "success",
                "message": "Cotizaciones devueltas con éxito",
                "cotizaciones": cotizaciones_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Cotizacion.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontraron cotizaciones para la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": ERROR_MESSAGE,
                "error": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, pk):
        try:
            solicitud = Solicitud.objects.get(id=pk)
            usuario = UserProfile.objects.get(user=request.user)
            data = request.data.copy()

            data['solicitud'] = solicitud.id
            data['usuario_creacion'] = usuario.id

            if 'fecha_coti' in data and data['fecha_coti']:
                fecha_str = data['fecha_coti']
                fecha_coti = datetime.strptime(fecha_str, "%d-%m-%Y").date()
                data['fecha_coti'] = fecha_coti

            file_coti = request.FILES.get('file_coti', None)
            data['file_coti'] = file_coti if file_coti else None

            serializer = CotizacionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Cotización creada exitosamente",
                    "data": {
                        "solicitud_id": pk,
                        "cotizacion_id": serializer.data['id']
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear la cotización, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear la cotización",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #delete de todas las cotizaciones de una solicitud por id
    def delete(self, request, pk):
        try:
            solicitud = Solicitud.objects.get(id=pk)
            cotizaciones = Cotizacion.objects.filter(solicitud=solicitud)
            cotizaciones.delete()
            response_data = {
                "status": "success",
                "message": "Cotizaciones eliminadas exitosamente"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudieron eliminar las cotizaciones",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
class FormularioCreateDetailAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SolicitudSerializer
    def get(self,request,pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            Formulario.objects.filter(solicitud=solicitud)
            SolicitudSerializer(solicitud, many=True)
            response_data = {
                "status": "success",
                "message": "Formularios devueltos con éxito",
                "formularios": Formulario.objects.filter(solicitud=pk_s).values()
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Formulario.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontraron formularios para la solicitud con id {pk_s}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": ERROR_MESSAGE,
                "error": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            #usuario = UserProfile.objects.get(user=request.user)
            #request.data['usuario_creacion'] = usuario.id
            data = request.data.copy()
            data['solicitud'] = solicitud.id
            file_compra = request.FILES.get('file_compra', None)
            certi_banco = request.FILES.get('certi_banco', None)
            data['file_compra'] = file_compra if file_compra else None
            data['certi_banco'] = certi_banco if certi_banco else None
            
            serializer = FormularioSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Formulario creado exitosamente",
                    "data": {
                        "solicitud_id": pk_s,
                        "formulario_id": serializer.data['id']
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear el formulario, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear el formulario",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET de todas las solicitudes y POST de una factura por id de la solicitud
class FacturaCreateListAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudSerializer
    def get(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            Factura.objects.filter(solicitud=solicitud)
            SolicitudSerializer(solicitud, many=True)
            response_data = {
                "status": "success",
                "message": "Facturas devueltas con éxito",
                "facturas": Factura.objects.filter(solicitud=pk_s).values()
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Factura.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontraron facturas para la solicitud con id {pk_s}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": ERROR_MESSAGE,
                "error": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            request.data['solicitud'] = solicitud.id
            serializer = FacturaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Factura creada exitosamente",
                    "data": {
                        "solicitud_id": pk_s,
                        "factura_id": serializer.data['id']
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear la factura, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }