# Generated by Django 5.0.6 on 2024-07-31 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitud', '0005_remove_cotizacion_descripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='codigo',
            field=models.CharField(max_length=18),
        ),
    ]
