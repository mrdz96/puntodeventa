from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q, Sum, Max
from .models import *
from django.db.models import OuterRef, Subquery
import datetime
from datetime import datetime,timedelta,date
from django.contrib.auth.models import Permission, Group, User
from django.db import connection

def replace_nones(auxarr):
    i = 0
    for a in auxarr:
        if a.replace(" ", "") == "None":
            auxarr[i] = ""
        i += 1
    return auxarr

class DTUsuarios(BaseDatatableView):
    columns = ['username']
    order_columns = ['username']

    def get_initial_queryset(self):
        users = User.objects.all().exclude(groups__name__in=[])
        return users


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(username__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            print("ID USER: "+str(item.id))
            roles = item.groups.all()
            roles_str = ""
            for r in roles:
                roles_str += r.name + "<br>"
            
            nombre = ""
            try:
                perfil = Perfil.objects.get(user__id=item.id)
                nombre = perfil.nombre +' '+ perfil.apellido
            except:
                perfil =""
                nombre = ""
            if perfil!="":
                if perfil.eliminado==False and item.id != 1:
                    data = [
                        item.id,
                        nombre,
                        roles_str
                    ]
                    auxarr = [
                        str(nombre),
                        #str(item.username),
                        roles_str,
                        '<a href="editar/'+ str(item.id) +'"><i class="fas fa-edit"></i></a>',
                        '<a href="javascript:void(0)" onclick="delete_obj(' + str(data) + ')"><i class="fas fa-trash"></i></a>',
                    ]
                    auxarr = replace_nones(auxarr)
                    json_data.append(auxarr)
        return json_data
        
class DTPuestos(BaseDatatableView):
    columns = ['name']
    order_columns = ['name']

    def get_initial_queryset(self):
        roles = Group.objects.all()
        return roles


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(name__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            data = [
                item.id,
                item.name,
            ]
            permisos = item.permissions.all()
            permisos_str = ""
            for p in permisos:
                permisos_str += p.name + "<br>"
            auxarr = [
                str(item.name),
                permisos_str,
                '<a href="editar/'+ str(item.id) +'"><i class="fas fa-edit"></i></a>',
                '<a href="javascript:void(0)" onclick="delete_obj(' + str(data) + ')"><i class="fas fa-trash"></i></a>',
            ]
            auxarr = replace_nones(auxarr)
            json_data.append(auxarr)
        return json_data

class DTProductos(BaseDatatableView):
    columns = ['id','nombre','descripcion','categoria','precio','']
    order_columns = ['id','nombre','descripcion','categoria','precio','']

    def get_initial_queryset(self):
        productos = Producto.objects.all().exclude(eliminado=True)
        return productos


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(nombre__icontains=search)|Q(descripcion__icontains=search)|Q(categoria__nombre__icontains=search)|Q(precio__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            data = [
                item.id,
                item.nombre,
                item.descripcion,
                item.precio,
                item.categoria.nombre
            ]
           
            auxarr = [
                str(item.nombre),
                str(item.descripcion),
                str(item.categoria.nombre),
                str(item.precio),
                '<a href="editar/'+ str(item.id) +'"><i class="fas fa-edit"></i></a>',
                '<a href="javascript:void(0)" onclick="delete_obj(' + str(data) + ')"><i class="fas fa-trash"></i></a>',
            ]
            auxarr = replace_nones(auxarr)
            json_data.append(auxarr)
        return json_data
class DTCategoriaProductos(BaseDatatableView):
    columns = ['nombre']
    order_columns = ['nombre']

    def get_initial_queryset(self):
        categorias = ProductoCategoria.objects.all()
        return categorias

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(nombre__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            data = [
                item.id,
                item.nombre,
            ]
           
            auxarr = [
                str(item.nombre),
                '<a href="editar/'+ str(item.id) +'"><i class="fas fa-edit"></i></a>',
                '<a href="javascript:void(0)" onclick="delete_obj(' + str(data) + ')"><i class="fas fa-trash"></i></a>',
            ]
            auxarr = replace_nones(auxarr)
            json_data.append(auxarr)
        return json_data
class DTVentas(BaseDatatableView):
    columns=['id','fecha','total']
    order_columns=['id','fecha','total']

    def get_initial_queryset(self):
        ventas = Venta.objects.all()
        return ventas
    def filter_queryset(self,qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(id__icontains=search)|Q(total__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            data = [
                item.id,
                item.fecha_registro,
                item.total,
            ]
            if item.estatus =="1":
                estatus = "En curso"
            elif item.estatus =="2":
                estatus = "Terminada"
            elif item.estatus == "3":
                estatus = "Cancelada"
            auxarr = [
                str(item.id),
                str(item.fecha_registro.strftime("%Y/%m/%d, %H:%M:%S")),
                str(estatus),
                str(item.total),
                '<a href="info/'+ str(item.id) +'" class="btn btn-info">Ver Detalles de la Venta</a>',
            ]
            auxarr = replace_nones(auxarr)
            json_data.append(auxarr)
        return json_data

class DTVentasRegistradas(BaseDatatableView):
    columns=['id','fecha','total']
    order_columns=['id','fecha','total']

    def get_initial_queryset(self):
        ventas = Venta.objects.all()
        ventas = ventas.filter(fecha_registro__icontains=datetime.today().strftime("%Y-%m-%d"))
        return ventas
    def filter_queryset(self,qs):
        #search = self.request.GET.get(u'search[value]', None)
        #if search:
        #    qs = qs.filter(Q(id__icontains=search)|Q(fecha__icontains=search)|Q(total__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.estatus == "1":
            
                data = [
                    item.id,
                    item.fecha_registro,
                    item.total,
                ]
            
                auxarr = [
                    str(item.id),
                    str(item.cliente),
                    str(item.fecha_registro.strftime("%Y/%m/%d, %H:%M:%S")),
                    "$"+str(item.total),
                    '<a href="ventas/info/'+ str(item.id) +'" class="btn btn-info">Ver Detalles de la Venta</a>',
                    '<button onclick="terminar_venta('+ str(item.id) +')" class="btn btn-success">Terminar Venta</button>',
                    '<button onclick="cancelar_venta('+ str(item.id) +')" class="btn btn-danger">Cancelar Venta</button>',
                    '<button onclick="agregar_producto('+ str(item.id) +')" class="btn btn-primary">Agregar Producto</button>',
                    '<button onclick="imprimir_cuenta('+ str(item.id) +')" class="btn btn-secondary">Cuenta del cliente</button>',
                    
                ]
                auxarr = replace_nones(auxarr)
                json_data.append(auxarr)
        return json_data
class DTVentasTerminadas(BaseDatatableView):
    columns=['id','fecha','total']
    order_columns=['id','fecha','total']

    def get_initial_queryset(self):
        ventas = Venta.objects.all()
        ventas = ventas.filter(fecha_terminado__icontains=datetime.today().strftime("%Y-%m-%d"))
        return ventas
    def filter_queryset(self,qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(id__icontains=search)|Q(fecha__icontains=search)|Q(total__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.estatus == "2":
                detalle = DetalleVenta.objects.filter(venta=item)
                detalletxt = ""
                cont = 1
                for prods in detalle:
                    producto = Producto.objects.get(id=prods.producto.id)
                    codigotxt = str(producto.id)
                    productotxt = str(producto.categoria.nombre) + " " + str(producto.nombre)
                    cantidadtxt = str(prods.cantidad)
                    preciotxt = str(producto.precio)
                    subtotaltxt = str(prods.subtotal)
                    detalletxt+=str(cont)+". Código: "+codigotxt+" - Producto: " + productotxt + " - Precio: $"+preciotxt+" - Cantidad: "+ cantidadtxt +" - Subtotal: $"+subtotaltxt+"<br>"
                    cont = cont+1

                data = [
                    item.id,
                    item.fecha_registro,
                    item.total,
                ]
            
                auxarr = [
                    str(item.id),
                    str(item.cliente),
                    str(item.fecha_terminado.strftime("%Y/%m/%d, %H:%M:%S")),
                    #str(detalletxt),
                    "$"+str(item.total),
                    '<a href="ventas/info/'+ str(item.id) +'" class="btn btn-info">Ver Detalles de la Venta</a>',
                ]
                auxarr = replace_nones(auxarr)
                json_data.append(auxarr)
        return json_data

class DTVentasCanceladas(BaseDatatableView):
    columns=['id','fecha','total']
    order_columns=['id','fecha','total']

    def get_initial_queryset(self):
        ventas = Venta.objects.all()
        ventas = ventas.filter(fecha_cancelado__icontains=datetime.today().strftime("%Y-%m-%d"))
        return ventas
    def filter_queryset(self,qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(id__icontains=search)|Q(fecha__icontains=search)|Q(total__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            if item.estatus == "3":
                detalle = DetalleVenta.objects.filter(venta=item)
                detalletxt = ""
                cont = 1
                for prods in detalle:
                    producto = Producto.objects.get(id=prods.producto.id)
                    codigotxt = str(producto.id)
                    productotxt = str(producto.categoria.nombre) + " " + str(producto.nombre)
                    cantidadtxt = str(prods.cantidad)
                    preciotxt = str(producto.precio)
                    subtotaltxt = str(prods.subtotal)
                    detalletxt+=str(cont)+". Código: "+codigotxt+" - Producto: " + productotxt + " - Precio: $"+preciotxt+" - Cantidad: "+ cantidadtxt +" - Subtotal: $"+subtotaltxt+"<br>"
                    cont = cont+1

                data = [
                    item.id,
                    item.fecha_registro,
                    item.total,
                ]
            
                auxarr = [
                    str(item.id),
                    str(item.cliente),
                    str(item.fecha_cancelado.strftime("%Y/%m/%d, %H:%M:%S")),
                    #str(detalletxt),
                    "$"+str(item.total),
                    '<a href="ventas/info/'+ str(item.id) +'" class="btn btn-info">Ver Detalles de la Venta</a>',
                ]
                auxarr = replace_nones(auxarr)
                json_data.append(auxarr)
        return json_data

class DTMenu(BaseDatatableView):
    columns = ['id','nombre','descripcion','categoria','precio','']
    order_columns = ['id','nombre','descripcion','categoria','precio','']

    def get_initial_queryset(self):
        productos = Producto.objects.all()
        return productos


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(nombre__icontains=search)|Q(descripcion__icontains=search)|Q(categoria__nombre__icontains=search)|Q(precio__icontains=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            data = [
                item.id,
                item.nombre,
                item.descripcion,
                item.precio,
                item.categoria.nombre
            ]
           
            auxarr = [
                str(item.id),
                str(item.nombre),
                str(item.descripcion),
                "$"+str(item.precio),
            ]
            auxarr = replace_nones(auxarr)
            json_data.append(auxarr)
        return json_data    


        