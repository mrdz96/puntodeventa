# Generated by Django 3.0.6 on 2021-03-04 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0004_auto_20210304_0308'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('pagado', models.FloatField(blank=True, null=True)),
                ('cambio', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
                ('descripcion', models.CharField(max_length=500)),
                ('precio', models.FloatField(blank=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.ProductoCategoria')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('precio_unitario', models.FloatField(blank=True, null=True)),
                ('subtotal', models.FloatField(blank=True, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.Producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system.Venta')),
            ],
        ),
    ]
