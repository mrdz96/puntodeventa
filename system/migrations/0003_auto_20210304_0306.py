# Generated by Django 3.0.6 on 2021-03-04 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='fecha_nacimento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
