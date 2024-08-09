from rest_framework import serializers
from .models import Solicitud, ItemSolicitud, Estado, Cotizacion, Formulario, Factura

class SolicitudSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Solicitud
        fields = ['id', 'codigo', 'nombre', 'tema', 'tipo', 'estado', 'fecha_creacion', 'proyecto', 'cotizacion_aceptada','usuario_creacion']
        read_only_fields = ['id', 'fecha_creacion', 'codigo']

    cotizacion_aceptada = serializers.PrimaryKeyRelatedField(
        queryset=Cotizacion.objects.all(), 
        required=False,
        allow_null=True)
    def create(self, validated_data):
        return Solicitud.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.tema = validated_data.get('tema', instance.tema)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.proyecto = validated_data.get('proyecto', instance.proyecto)
        
        if 'cotizacion_aceptada' in validated_data:
            instance.cotizacion_aceptada = validated_data.get('cotizacion_aceptada')

        instance.save()
        return instance

class ItemSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSolicitud
        fields = ['id', 'item', 'solicitud', 'fecha_creacion', 'descripcion', 'cantidad', 'unidad']
        read_only_fields = ['id', 'fecha_creacion']

    def create(self, validated_data):
        return ItemSolicitud.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.item = validated_data.get('item', instance.item)
        instance.solicitud = validated_data.get('solicitud', instance.solicitud)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.unidad = validated_data.get('unidad', instance.unidad)
        instance.fecha_creacion = validated_data.get('fecha_creacion', instance.fecha_creacion)
        instance.save()
        return instance

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['id', 'nombre', 'mensaje']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Estado.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.mensaje = validated_data.get('mensaje', instance.mensaje)
        instance.save()
        return instance

class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = ['id', 'solicitud', 'monto','proveedor','no_coti','monto','url_coti','fecha_coti']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Cotizacion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solicitud = validated_data.get('solicitud', instance.solicitud)
        instance.monto = validated_data.get('monto', instance.monto)
        instance.proveedor = validated_data.get('proveedor', instance.proveedor)
        instance.no_coti = validated_data.get('no_coti', instance.no_coti)
        instance.monto = validated_data.get('monto', instance.monto)
        instance.url_coti = validated_data.get('url_coti', instance.url_coti)
        instance.fecha_coti = validated_data.get('fecha_coti', instance.fecha_coti)
        instance.save()
        return instance
    
class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = [
            'id', 
            'solicitud', 
            'cedula_ruc', 
            'tipo_compra', 
            'no_compra', 
            'url_compra', 
            'tipo_acuerdo', 
            'forma_pago', 
            'tipo_pago', 
            'tiempo', 
            'url_certi_banco', 
            'anticipo',
            'nombre_banco', 
            'tipo_cuenta', 
            'numero_cuenta',
            'nombre_cuenta', 
            'correo'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        return Formulario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solicitud = validated_data.get('solicitud', instance.solicitud)
        instance.cedula_ruc = validated_data.get('cedula_ruc', instance.cedula_ruc)
        instance.tipo_compra = validated_data.get('tipo_compra', instance.tipo_compra)
        instance.no_compra = validated_data.get('no_compra', instance.no_compra)
        instance.url_compra = validated_data.get('url_compra', instance.url_compra)
        instance.tipo_acuerdo = validated_data.get('tipo_acuerdo', instance.tipo_acuerdo)
        instance.forma_pago = validated_data.get('forma_pago', instance.forma_pago)
        instance.tipo_pago = validated_data.get('tipo_pago', instance.tipo_pago)
        instance.tiempo = validated_data.get('tiempo', instance.tiempo)
        instance.url_certi_banco = validated_data.get('url_certi_banco', instance.url_certi_banco)
        instance.anticipo = validated_data.get('anticipo', instance.anticipo)
        instance.nombre_banco = validated_data.get('nombre_banco', instance.nombre_banco)
        instance.tipo_cuenta = validated_data.get('tipo_cuenta', instance.tipo_cuenta)
        instance.numero_cuenta = validated_data.get('numero_cuenta', instance.numero_cuenta)
        instance.nombre_cuenta = validated_data.get('nombre_cuenta', instance.nombre_cuenta)
        instance.correo = validated_data.get('correo', instance.correo)
        instance.save()
        return instance

    
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id','solicitud','estado','monto','comentario']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Factura.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solicitud = validated_data.get('solicitud', instance.solicitud)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.monto = validated_data.get('monto', instance.monto)
        instance.comentario = validated_data.get('comentario', instance.comentario)
        instance.save()
        return instance