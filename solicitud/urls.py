from django.urls import path
from . import views

urlpatterns = [
    path('solicitudes/all/', views.SolicitudGetAllAPIView.as_view(), name='solicitudes-all'),
    path('solicitudes/<int:pk>/', views.SolicitudDetailAPIView.as_view(), name='detalle-solicitud'),
    path('solicitudes/', views.SolicitudByUserAPIView.as_view(), name='solicitudes-usuario'),

    path('solicitudes/<int:pk>/cotizaciones/', views.CotizacionListCreateDeleteAPIView.as_view(), name='cotizaciones-solicitud'),

    path('proyectos/<int:pk>/solicitud/', views.SolicitudCreateAPIView.as_view(), name='crear-solicitud'),
    path('proyecto/<int:pk_p>/<int:pk_s>/estado/', views.EstadoListAPIView.as_view(), name='estado-solicitud'),
    path('proyecto/<int:pk_p>/solicitud/<int:pk_s>/estado/<int:pk_e>/', views.EstadoUpdateAPIView.as_view(), name='estado-solicitud'),

    path('formulario/<int:pk_s>/', views.FormularioCreateDetailAPIView.as_view(), name='crear-formulario'),

    path('solicitud/<int:pk_s>/factura/', views.FacturaCreateListAPIView.as_view(), name='crear-detalle-factura'),

    path('solicitudes/<pk_s>/items/', views.ItemSolicitudListCreateAPIView.as_view(), name='crear-items-solicitud'),
]