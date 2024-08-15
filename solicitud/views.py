from datetime import datetime
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Solicitud, ItemSolicitud, Estado, Cotizacion, Formulario, Factura
from .serializers import SolicitudSerializer, ItemSolicitudSerializer, CotizacionSerializer, FormularioSerializer, FacturaSerializer
from proyecto.models import Proyecto
from user.models import UserProfile


# Create your views here.
ERROR_MESSAGE = "Fallo en la consulta"

#crear una solicitud de un proyecto YA EXISTENTE y GET de todas las solicitudes
class SolicitudCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudSerializer
    def post(self, request, pk):
        try:
            proyecto = Proyecto.objects.get(id=pk)
            usuario = UserProfile.objects.get(user=request.user)
            usuario_modi = UserProfile.objects.get(user=request.user)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            request.data['proyecto'] = proyecto.id
            request.data['usuario_creacion'] = usuario.id
            request.data['usuario_modificacion'] = usuario_modi.id
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
            usuario_modi = UserProfile.objects.get(user=request.user)
            cotizacion_aceptada = request.data.get('cotizacion_aceptada')
            coti_nueva = Cotizacion.objects.get(id=cotizacion_aceptada) 
            if not cotizacion_aceptada:
                response_data = {
                    "status": "error",
                    "message": "Se necesita un valor 'cotizacion_aceptada' para realizar la actualización"
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Cotizacion.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró la cotización con id {cotizacion_aceptada}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            data = request.data.copy()
            data['cotizacion_aceptada'] = coti_nueva.id
            data['usuario_modificacion'] = usuario_modi.id
            serializer = SolicitudSerializer(solicitud, data=data, partial=True)

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
    
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo actualizar la solicitud",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
class CotizacionListCreateDeleteAPIView(APIView):
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
                    "url_coti": cotizacion.url_coti if cotizacion.url_coti else None
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
    permission_classes = [IsAuthenticated]
    serializer_class = FormularioSerializer  # Cambié esto para que use el serializador correcto
    
    def get(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            formularios = Formulario.objects.filter(solicitud=solicitud)
            if not formularios.exists():
                raise Formulario.DoesNotExist
            response_data = {
                "status": "success",
                "message": "Formularios devueltos con éxito",
                "formularios": formularios.values()
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Formulario.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"No se encontraron formularios para la solicitud con id {pk_s}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            data = request.data.copy()
            data['solicitud'] = solicitud.id
            
            # Asumiendo que estás enviando URLs y no archivos
            data['url_compra'] = data.get('url_compra')
            data['url_certi_banco'] = data.get('url_certi_banco')
            
            serializer = FormularioSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Formulario creado exitosamente",
                    "data": {
                        "solicitud_id": pk_s,
                        "formulario_id": serializer.data['id']
                    }
                }, status=status.HTTP_201_CREATED)
            return Response({
                "status": "error",
                "message": "No se pudo crear el formulario, error del serializer",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET de todas las solicitudes y POST de una factura por id de la solicitud y PUT 
class FacturaCreateListAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FacturaSerializer
    def get_queryset(self):
        return Factura.objects.filter(solicitud__id=self.kwargs['pk_s'])
    
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
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear la factura",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, pk_s):
        try:
            solicitud = Solicitud.objects.get(id=pk_s)
            request.data['solicitud'] = solicitud.id
            factura = self.get_queryset().first()  # Obtén la primera factura asociada a la solicitud
            if not factura:
                return Response({
                    "status": "error",
                    "message": f"No se encontró ninguna factura asociada a la solicitud con id {pk_s}"
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(factura, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Factura actualizada exitosamente",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "No se pudo actualizar la factura, error del serializer",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Solicitud.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"No se encontró la solicitud con id {pk_s}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
