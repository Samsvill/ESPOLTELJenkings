from rest_framework import serializers
from .models import Solicitud, Estado, Cotizacion, Formulario, Factura

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
        instance.cotizacion_aceptada = validated_data.get('cotizacion_aceptada', instance.cotizacion) if validated_data.get('cotizacion_aceptada') is not None else None
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
        fields = ['id', 'solicitud', 'monto','proveedor','no_coti','monto','file_coti','fecha_coti']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Cotizacion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solicitud = validated_data.get('solicitud', instance.solicitud)
        instance.monto = validated_data.get('monto', instance.monto)
        instance.proveedor = validated_data.get('proveedor', instance.proveedor)
        instance.no_coti = validated_data.get('no_coti', instance.no_coti)
        instance.monto = validated_data.get('monto', instance.monto)
        instance.file_coti = validated_data.get('file_coti', instance.file_coti)
        instance.fecha_coti = validated_data.get('fecha_coti', instance.fecha_coti)
        instance.save()
        return instance
    
class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = ['id',
                  'solicitud',
                  'cedula_ruc',
                  'tipo_compra',
                  'no_compra',
                  'file_compra',

                  'tipo_acuerdo',
                  'forma_pago',
                  'tipo_pago',
                  'tiempo',
                  'certi_banco',
                  'anticipo',

                  'nombre_banco',
                  'tipo_cuenta',
                  'numero_cuenta',
                  'nombre_cuenta',
                  'correo',]
        read_only_fields = ['id']

    def create(self, validated_data):
        return Formulario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.solicitud = validated_data.get('solicitud', instance.solicitud)
        instance.cedula_ruc = validated_data.get('cedula_ruc', instance.cedula_ruc)
        instance.tipo_compra = validated_data.get('tipo_compra', instance.tipo_compra)
        instance.no_compra = validated_data.get('no_compra', instance.no_conmpra)
        instance.file_compra = validated_data.get('file_compra', instance.file_compra)

        instance.tipo_acuerdo = validated_data.get('tipo_acuerdo', instance.tipo_acuerdo)
        instance.forma_pago = validated_data.get('forma_pago', instance.forma_pago)
        instance.tipo_pago = validated_data.get('tipo_pago', instance.tipo_pago)
        instance.tiempo = validated_data.get('tiempo', instance.tiempo)
        instance.certi_banco = validated_data.get('certi_banco', instance.certi_banco)
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