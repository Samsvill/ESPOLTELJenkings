# Generated by Django 5.0.6 on 2024-07-24 04:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0002_delete_solicitud'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='proyectos', to='user.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='budgetitem',
            name='valor',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('codigo', models.CharField(max_length=15)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('tema', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='proyecto.proyecto')),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
