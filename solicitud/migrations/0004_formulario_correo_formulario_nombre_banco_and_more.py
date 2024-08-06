# Generated by Django 5.0.6 on 2024-07-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0003_alter_solicitud_codigo_formulario'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='correo',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='formulario',
            name='nombre_banco',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='formulario',
            name='nombre_cuenta',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='formulario',
            name='numero_cuenta',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='formulario',
            name='tipo_cuenta',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
