from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name="userrole_user")
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username

class Perfil(models.Model):
    nombre = models.CharField(max_length=500)
    apellido = models.CharField(max_length=500, blank=True)
    tel1 = models.CharField(max_length=500, blank=True, null=True)
    correo = models.EmailField(max_length=500, blank=True, null=True)
    fecha_nacimento = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    eliminado = models.BooleanField(default=False)
    def __str__(self):
        return str(self.nombre)

class ProductoCategoria(models.Model):
    nombre = models.CharField(max_length=500)
    def __str__(self):
        return str(self.nombre)

class Producto(models.Model):
    nombre = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=500)
    precio = models.FloatField(blank=True, null=True)
    categoria = models.ForeignKey(ProductoCategoria,on_delete=models.PROTECT,blank=True, null=True)
    eliminado = models.BooleanField(default=False)
    def __str__(self):
        return str(self.nombre)

class Venta(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.PROTECT,blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    fecha_cancelado = models.DateTimeField(blank=True, null=True)
    fecha_terminado = models.DateTimeField(blank=True, null=True)
    pagado = models.FloatField(blank=True,null=True)
    cambio = models.FloatField(blank=True,null=True)
    total = models.FloatField(blank=True,null=True)
    motivo_cancelado = models.CharField(max_length=500,null=True,blank=True)
    lista_estatus = (
        ("1", 'Registrada'),
        ("2", 'Terminada'),
        ("3", 'Cancelada'),
    )
    estatus = models.CharField(max_length=2, choices=lista_estatus, default=1)
    cliente = models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return str(self.id)

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT,blank=True, null=True)
    venta = models.ForeignKey(Venta,on_delete=models.PROTECT,blank=True, null=True)
    cantidad = models.IntegerField(blank=True,null=True)
    precio_unitario = models.FloatField(blank=True,null=True)
    subtotal = models.FloatField(blank=True,null=True)
    def __str__(self):
        return str(self.id)

class Paquete(models.Model):
    nombre = models.CharField(max_length=500)
    precio = models.FloatField(blank=True,null=True)
    def __str__(self):
        return str(self.nombre)
        
class PaqueteProducto(models.Model):
    paquete = models.ForeignKey(Paquete,on_delete=models.PROTECT,blank=True, null=True)
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT,blank=True, null=True)
    cantidad = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return str(self.id)
