# Generated by Django 3.0.6 on 2021-03-04 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_detalleventa_producto_productocategoria_venta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
                ('precio', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaqueteProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.Paquete')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.Producto')),
            ],
        ),
    ]
