from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, ContentType, Group
from .models import *
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import user_passes_test

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
import json
from datetime import datetime,timedelta,date
from django.db.models import Q, Sum, Max, Min
import traceback
###Mail
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import traceback
#Descargas
import tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import io
from io import StringIO,BytesIO
#import PIL
#from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

@login_required(login_url='/mrchampions/login')
def index(request):
    ventas_encurso = Venta.objects.filter(estatus=1,fecha_registro__icontains=datetime.today().strftime("%Y-%m-%d"))
    ventas_terminadas = Venta.objects.filter(estatus=2, fecha_terminado__icontains=datetime.today().strftime("%Y-%m-%d"))
    ventas_canceladas = Venta.objects.filter(estatus=3, fecha_cancelado__icontains=datetime.today().strftime("%Y-%m-%d"))

    ventas_terminadas_hoy = Venta.objects.filter(estatus=2,fecha_terminado__icontains=datetime.today().strftime("%Y-%m-%d"))
    ganancias_hoy = 0
    for ventas_g in ventas_terminadas_hoy:
        ganancias_hoy = ganancias_hoy + ventas_g.total
    ventas_terminadas_totales = Venta.objects.filter(estatus=2)
    ganancias_totales = 0
    for ventas_t in ventas_terminadas_totales:
        ganancias_totales = ganancias_totales + ventas_t.total
    productos = Producto.objects.all()
    return render(request,'index/index.html',{'ventas_encurso':ventas_encurso.count(),'ventas_terminadas':ventas_terminadas.count(),'ventas_canceladas':ventas_canceladas.count(),
        'ventas_terminadas_hoy':ventas_terminadas_hoy.count(),'ganancias_hoy':ganancias_hoy,'ventas_terminadas_totales':ventas_terminadas_totales.count(),'ganancias_totales':ganancias_totales,
        'productos':productos})


def login_page(request):
	#print("entre")
	return render(request,'login/login.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            #usrol = UserRole.objects.filter(user=user).latest('id')
            #request.session['rol'] = usrol.role.name
            role = ""
            if user.groups.all().exists():
                usrol = user.groups.all().latest('id')
                role = usrol.name
            login(request, user)
            request.session['rol'] = role
            request.session['menus'] = get_menu_permission(request)
            permissions = Permission.objects.filter(user=request.user)
            perfil = Perfil.objects.get(user__id=user.id)
            request.session['nombre'] = perfil.nombre +" "+ perfil.apellido
            return redirect('/mrchampions')
        else:
            return render(request,'login/login.html',{'error': True, 'message': 'Nombre de usuario o contraseña incorrecta.'})

@login_required(login_url='/mrchampions/login')
def logout_user(request):
    logout(request)
    return redirect('/mrchampions/login')

def get_menu_permission(request):
    menus = [
        {
            'nombre': "Usuarios",
            'has_perm': True,
            'icon': 'fas fa-user',
            'menu': [
                {
                    'nombre': 'Empleados',
                    'permiso': 'system.usuarios-lista',
                    'url': 'usuarios_lista',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Registrar Empleados',
                    'permiso': 'system.usuarios-lista',
                    'url': 'usuarios_insertar',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Puestos',
                    'permiso': 'system.puestos-lista',
                    'url': 'puestos_lista',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Agregar Puestos',
                    'permiso': 'system.puestos-lista',
                    'url': 'puestos_insertar',
                    'multi_menu': False,
                    'has_perm': False,
                }
               
            ]
        },{
            'nombre': "Productos",
            'has_perm': True,
            'icon': 'fas fa-user',
            'menu': [
                {
                    'nombre': 'Productos',
                    'permiso': 'system.productos-lista',
                    'url': 'productos_lista',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Registrar Producto',
                    'permiso': 'system.productos-lista',
                    'url': 'productos_insertar',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Categorias de Productos',
                    'permiso': 'system.productos-lista',
                    'url': 'categoria_productos_lista',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Agregar Categoria de Producto',
                    'permiso': 'system.productos-lista',
                    'url': 'categoria_productos_insertar',
                    'multi_menu': False,
                    'has_perm': False,
                }
               
            ]
        },{
            'nombre': "Ventas",
            'has_perm': True,
            'icon': 'fas fa-user',
            'menu': [
                {
                    'nombre': 'Listado de Ventas',
                    'permiso': 'system.ventas-lista',
                    'url': 'ventas_lista',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Realizar Nueva Venta',
                    'permiso': 'system.ventas-lista',
                    'url': 'ventas_insertar',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Ventas en Proceso',
                    'permiso': 'system.ventas-lista',
                    'url': 'categoria_productos_lista',
                    'multi_menu': False,
                    'has_perm': False,
                },{
                    'nombre': 'Ventas Terminadas',
                    'permiso': 'system.ventas-lista',
                    'url': 'categoria_productos_insertar',
                    'multi_menu': False,
                    'has_perm': False,
                }
               
            ]
        }

    ]
    # try:
    #     user = request.user
    #     count1 = 0
    #     for menu in menus:
    #         has_perm_menu = True
    #         count2 = 0
    #         for submenu in menu['menu']:
    #             if submenu['multi_menu'] == False:
    #                 if user.has_perm(submenu['permiso']):
    #                     menus[count1]['menu'][count2]['has_perm'] = True
    #                     has_perm_menu = True
    #             else:
    #                 count3 = 0
    #                 has_perm_submenu = True
    #                 for subsubmenu in submenu['submenu']:
    #                     if user.has_perm(subsubmenu['permiso']):
    #                         menus[count1]['menu'][count2]['submenu'][count3]['has_perm'] = True
    #                         has_perm_submenu = True
    #                         has_perm_menu = True
    #                     count3 += 1
    #                 menus[count1]['menu'][count2]['has_perm'] = has_perm_submenu
    #             count2 += 1
    #         menus[count1]['has_perm'] = has_perm_menu
    #         count1 += 1
    return menus
    # except Exception as e:
        # return menus
def permission_required_2(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        #return HttpResponseNotFound()
        return False
    return user_passes_test_2(check_perms, login_url=login_url)
def user_passes_test_2(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                #if request.user.is_authenticated:
                #    return HttpResponseNotFound()
                return view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                return HttpResponseNotFound()
            else:
                path = request.build_absolute_uri()
                resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
                current_scheme, current_netloc = urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme) and
                        (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(
                    path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator
@login_required(login_url='/almacen/login')
def get_permiso_visualizacion(request):    
    message = {"error": False, "message": "", "data": []}

    try:
        usuario = request.user
        user_group = usuario.groups.all().latest('id')
        obj_grupo = Group.objects.get(id=int(user_group.id))
        permiso_calendario = obj_grupo.permissions.filter(codename="solo-visualizar")
        if len(permiso_calendario) == 0:
            message['message'] = False
        else:
            message['message'] = True
    except Exception as e:
        print(e)
        message['message'] = False

    
    return JsonResponse(message)


#USUARIOS
@login_required(login_url='/mrchampions/login')
def usuarios_lista(request):
    return render(request,'usuarios/list.html',)

@login_required(login_url='/mrchampions/login')
def usuarios_editar(request,id):
    try:
        user = User.objects.get(id=int(id))
        puestos_seleccionados = list(user.groups.all().values_list('id', flat=True))
        puestos = Group.objects.all().exclude(name__in=[])
        puestos_list = []
        for p in puestos:
            selec = False
            if p.id in puestos_seleccionados:
                selec = True
            puestos_list.append({
                'id': p.id,
                'name': p.name,
                'seleccionado': selec,
            })
        perfil = Perfil.objects.get(user__id=user.id)  
        fecha = perfil.fecha_nacimento.strftime("%Y-%m-%d")
        return render(request,'usuarios/form_edit.html',{'obj':user,'puestos':puestos_list,'perfil':perfil ,'fecha':fecha})
    except Exception as e:
        print(str(e))
        return HttpResponseNotFound()
    

@login_required(login_url='/mrchampions/login')
def usuarios_editar_save(request):
    try:
        id = request.POST.get('id','')
        
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        correo = request.POST.get('correo', '')
        tel1 = request.POST.get('tel1', '')
        fecha = request.POST.get('fecha','')
        username = request.POST.get('username', '')
        password = request.POST.get('password','')
        puestos = request.POST.getlist('roles', '')
        puestos_list = Group.objects.filter(id__in=puestos)

        user = User.objects.get(id=int(id))
        if puestos_list.count() > 0:
            user.groups.clear()
            user.groups.set(puestos_list)
        if username!="" and username!=None:
            user.username = username
        if password!="" and password!=None:
            user.set_password(password)
        user.save()

        ##Agrear Perfil
        perfil = Perfil.objects.get(user__id=user.id)
        if nombre!="" and nombre !=None:
            perfil.nombre = nombre
        if apellido!="" and apellido !=None:
            perfil.apellido = apellido
        if correo!="" and correo !=None:
            perfil.correo = correo
        if tel1!="" and tel1 !=None:
            perfil.tel1 = tel1   
        if fecha!="" and fecha !=None:
            perfil.fecha_nacimento = fecha
        perfil.save()
        messages.error(request, 'Empleado registrado correctamente', extra_tags='success')
        return redirect('usuarios_lista')
    except Exception as e:
        messages.error(request, 'Error registrando empleado: ' + str(e), extra_tags='danger')
        return redirect('usuarios_lista') 

@login_required(login_url='/mrchampions/login')
def usuarios_eliminar(request):
    try:
        idusuario = request.POST.get('id','')
        usuario = User.objects.get(id = idusuario)
        usuario.username = ""
        usuario.password = ""
        usuario.save()
        perfil = Perfil.objects.get(user = usuario)
        perfil.eliminado = True
        perfil.save()
        messages.error(request, 'Empleado eliminado correctamente', extra_tags='success')
        return redirect('usuarios_lista')
    except Exception as e:
        messages.error(request, 'Error eliminando empleado: ' + str(e), extra_tags='danger')
        return redirect('usuarios_lista')

@login_required(login_url='/mrchampions/login')
def usuarios_insertar(request):
    try:
        puestos = Group.objects.all().exclude(name__in=[])
        puestos_list = []
        for p in puestos:
            puestos_list.append({
                'id': p.id,
                'name': p.name,
            })
        return render(request,'usuarios/form.html',{'puestos':puestos_list})
    except Exception as e:
        return HttpResponseNotFound()
@login_required(login_url='/mrchampions/login')
def usuarios_insertar_save(request):
    try:
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        correo = request.POST.get('correo', '')
        tel1 = request.POST.get('tel1', '')
        fecha = request.POST.get('fecha','')
        username = request.POST.get('username', '')
        password = request.POST.get('password','')
        puestos = request.POST.getlist('roles', '')

        puestos_list = Group.objects.filter(id__in=puestos)
        user = User.objects.create_user(username, None, password)
        if puestos_list.count() > 0:
            user.groups.clear()
            user.groups.set(puestos_list)
        user.username = username
        user.save()

        ##Agrear Perfil
        perfil = Perfil(nombre = nombre,apellido=apellido,user=user,tel1=tel1,correo=correo,fecha_nacimento=fecha)
        perfil.save()
        messages.error(request, 'Empleado registrado correctamente', extra_tags='success')
        return redirect('usuarios_lista')
    except Exception as e:
        messages.error(request, 'Error registrando empleado: ' + str(e), extra_tags='danger')
        return redirect('usuarios_lista')   



#PUESTOS
@login_required(login_url='/mrchampions/login')
def puestos_lista(request):
    return render(request,'puestos/list.html',)

@login_required(login_url='/mrchampions/login')
def puestos_editar(request,id):
    try:
        obj = Group.objects.get(id=int(id))
        permi_selected = list(obj.permissions.all().values_list('id', flat=True))
        permissions_list = []
        permissions = Permission.objects.filter(content_type__model='all')
        for p in permissions:
            select = False
            if p.id in permi_selected:
                select = True
            permissions_list.append({
                'id': p.id,
                'codename': p.codename,
                'name': p.name,
                'seleccionado': select,
            })
        return render(request, 'puestos/form_edit.html', {'permissions': permissions_list, 'obj': obj})
    except Exception as e:
        print(str(e))
        return HttpResponseNotFound()

@login_required(login_url='/mrchampions/login')
def puestos_editar_save(request):
    try:
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        permissions = request.POST.getlist('permissions', '')
        obj = Group.objects.get(id=int(id))
        obj.name = name
        permi_selected = obj.permissions.all()
        for p in permi_selected:
            obj.permissions.remove(p)
        permissions_list = Permission.objects.filter(id__in=permissions)
        obj.permissions.set(permissions_list)
        obj.save()
        messages.error(request, 'Rol editado correctamente.', extra_tags='success')
        return redirect('puestos_lista')
    except Exception as e:
        messages.error(request, 'Error editando rol: ' + str(e), extra_tags='danger')
        return redirect('puestos_lista')

@login_required(login_url='/mrchampions/login')
def puestos_insertar(request):
    permissions = Permission.objects.filter(content_type__model='all')
    return render(request,'puestos/form.html',{'permissions': permissions})

@login_required(login_url='/mrchampions/login')
def puestos_insertar_save(request):
    try:
        name = request.POST.get('name', '')
        permissions = request.POST.getlist('permissions', '')
        permissions_list = Permission.objects.filter(id__in=permissions)
        group = Group(name=name)
        group.save()
        group.permissions.set(permissions_list)
        group.save()
        messages.error(request, 'Puesto creado correctamente.', extra_tags='success')
        return redirect('puestos_lista')
    except Exception as e:
        messages.error(request, 'Error creando puesto: ' + str(e), extra_tags='danger')
        return redirect('puestos_lista') 

@login_required(login_url='/mrchampions/login')
def puestos_eliminar(request):
    try:
        id = request.POST.get('id', '')
        obj = Group.objects.get(id=int(id))
        obj.delete()
        messages.error(request, 'Puesto eliminado correctamente.', extra_tags='success')
        return redirect('puestos_lista')
    except Exception as e:
        messages.error(request, 'Error eliminando puesto: ' + str(e), extra_tags='danger')
        return redirect('puestos_lista')

#PRODUCTOS
@login_required(login_url='/mrchampions/login')
def productos_lista(request):
    return render(request,'productos/list.html')


@login_required(login_url='/mrchampions/login')
def productos_insertar(request):
    categorias = ProductoCategoria.objects.all()
    return render(request,'productos/form.html',{'categorias':categorias})

@login_required(login_url='/mrchampions/login')
def productos_insertar_save(request):
    try:
        nombre = request.POST.get('nombre','')
        descripcion = request.POST.get('descripcion','')
        id_categoria = request.POST.get('categoria','')
        precio = request.POST.get('precio','')

        print(nombre)
        print(descripcion)
        print(id_categoria)
        print(precio)
            
        categoria = ProductoCategoria.objects.get(id=id_categoria)

        producto = Producto.objects.create()
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.categoria=categoria
        if precio!="" and producto!=None:
            producto.precio = precio
        else:
            producto.precio = 0.0
        producto.save()
        messages.error(request, 'Producto agregado correctamente.', extra_tags='success')
        return redirect('productos_lista')
    except Exception as e:
        messages.error(request, 'Error agregando producto: ' + str(e), extra_tags='danger')
        return redirect('productos_lista')

    
   #return render(request,'productos/form.html',{'categorias':categorias})


@login_required(login_url='/mrchampions/login')
def productos_editar(request,id):
    producto = Producto.objects.get(id=id)
    categorias = ProductoCategoria.objects.all()
    return render(request,'productos/form_edit.html',{'categorias':categorias,'producto':producto})

@login_required(login_url='/mrchampions/login')
def productos_editar_save(request):
    try:
        idprod = request.POST.get('id','')
        nombre = request.POST.get('nombre','')
        descripcion = request.POST.get('descripcion','')
        id_categoria = request.POST.get('categoria','')
        precio = request.POST.get('precio','')
        
        

        categoria = ProductoCategoria.objects.get(id=id_categoria)

        producto = Producto.objects.get(id=int(idprod))
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.categoria=categoria
        if precio!="" and producto!=None:
            producto.precio = precio
        else:
            producto.precio = 0.0
        producto.save()
        messages.error(request, 'Producto editado correctamente.', extra_tags='success')
        return redirect('productos_lista')
    except Exception as e:
        messages.error(request, 'Error editando producto: ' + str(e), extra_tags='danger')
        return redirect('productos_lista')
@login_required(login_url='/mrchampions/login')
def productos_eliminar(request):
    try:
        idprod = request.POST.get('id','')
        producto = Producto.objects.get(id=int(idprod))
        producto.eliminado = True
        producto.save()
        messages.error(request, 'Producto eliminado correctamente.', extra_tags='success')
        return redirect('productos_lista')
    except Exception as e:
        messages.error(request, 'Error eliminando producto: ' + str(e), extra_tags='danger')
        return redirect('productos_lista')


#CATEGORIAS PRODUCTOS
@login_required(login_url='/mrchampions/login')
def categoria_productos_lista(request):
    return render(request,'categoria_productos/list.html')


@login_required(login_url='/mrchampions/login')
def categoria_productos_insertar(request):
    categorias = ProductoCategoria.objects.all()
    return render(request,'categoria_productos/form.html',{'categorias':categorias})

@login_required(login_url='/mrchampions/login')
def categoria_productos_insertar_save(request):
    try:
        nombre = request.POST.get('nombre','')
        categoria = ProductoCategoria.objects.create()
        categoria.nombre=nombre
        categoria.save()
        messages.error(request, 'Categoria agregada correctamente.', extra_tags='success')
        return redirect('categoria_productos_lista')
    except Exception as e:
        messages.error(request, 'Error agregando categoria: ' + str(e), extra_tags='danger')
        return redirect('categoria_productos_lista')

#VENTAS
@login_required(login_url='/mrchampions/login')
def ventas_lista(request):
    return render(request,'ventas/list.html')


@login_required(login_url='/mrchampions/login')
def ventas_insertar(request):
    
    productos = Producto.objects.all()

    return render(request,'ventas/form.html',{'productos':productos})

@login_required(login_url='/mrchampions/login')
def ventas_agregar_producto(request):

    return render(request,'ventas/form.html',{'productos':productos})
@login_required(login_url='/mrchampions/login')
def ventas_registrar_save(request):
    try:
        total_venta = request.POST['total_to_send']
        productos_venta = request.POST['productos_to_send']
        cliente_nombre = request.POST['cliente_nombre_tosend']
        prodsarr = productos_venta.split(",")
        print(str(total_venta))
        print(len(prodsarr))
        cont = 0
        data =[]
        venta = Venta.objects.create()
        venta.usuario = request.user
        venta.fecha_registro = datetime.today()
        venta.total = total_venta
        venta.estatus="1"
        venta.cliente = cliente_nombre
        venta.save()

        for i in range(len(prodsarr)):
            
            if cont == 3:
                detalle = DetalleVenta.objects.create()
                detalle.venta = venta
                producto  = Producto.objects.get(id = prodsarr[i-3])
                detalle.producto = producto
                detalle.precio_unitario = producto.precio
                detalle.cantidad = prodsarr[i-2]
                detalle.subtotal = prodsarr[i-1]
                detalle.save()
                cont = 0
            else:
                cont = cont + 1

        messages.error(request, 'Venta registrada correctamente.', extra_tags='success')
        return redirect('index')
    except Exception as e:
        messages.error(request, 'Error al registrar venta: ' + str(e), extra_tags='danger')
        return redirect('index')

@login_required(login_url='/mrchampions/login')
def ventas_info(request,id):
    
    venta = Venta.objects.get(id = id)
    detalle = DetalleVenta.objects.filter(venta=venta)
    return render(request,'ventas/info.html',{'venta':venta,'detalle':detalle})

@login_required(login_url='/mrchampions/login')
def ventas_cancelar_save(request):
    try:
        idventa = request.POST['id']
        venta = Venta.objects.get(id=int(idventa))
        venta.estatus = "3"
        venta.fecha_cancelado = datetime.today()
        venta.save()

        messages.error(request, 'Venta cancelada correctamente.', extra_tags='success')
        return redirect('index')
    except Exception as e:
        messages.error(request, 'Error al cancelar venta: ' + str(e), extra_tags='danger')
        return redirect('index')

@login_required(login_url='/mrchampions/login')
def ventas_terminar_save(request):
    data = []
    try:
        idventa = request.GET['idterminarventa']
        pagado = request.GET['pagado_tosend']
        cambio = request.GET['cambio_tosend']
        venta = Venta.objects.get(id=int(idventa))
        venta.pagado = pagado
        venta.cambio = cambio
        venta.estatus = "2"
        venta.fecha_terminado = datetime.today()
        venta.save()
        detalleventa = DetalleVenta.objects.filter(venta=venta)
        data2 = []
        for i in detalleventa:
            data2.append({
                'producto':str(i.producto.nombre),
                'cantidad':str(i.cantidad),
                'precio':str(i.subtotal),
            })
        data.append({
            'id':str(venta.id),
            'fecha':str(venta.fecha_terminado),
            'total':str(venta.total),
            'cliente':str(venta.cliente),
            'pagado':str(venta.pagado),
            'cambio':str(venta.cambio),
            'productos':data2
        })
        return JsonResponse({'data':data})
        #messages.error(request, 'Venta cancelada correctamente.', extra_tags='success')
        #return redirect('index')
    except Exception as e:
        return JsonResponse({'data':'','venta':''})
        #messages.error(request, 'Error al cancelar venta: ' + str(e), extra_tags='danger')
        #return redirect('index')

@login_required(login_url='/mrchampions/login')
def getProductoInfo(request):
    try:
        info=[]
        idprod = request.GET.get('idprod','')
        producto = Producto.objects.get(id=idprod)
        info.append({
            'codigo':producto.id,
            'categoria':producto.categoria.nombre,
            'nombre':producto.nombre,
            'descripcion':producto.descripcion,
            'precio':producto.precio
        })
        return JsonResponse({'info':info})
    except:
        return JsonResponse({})

@login_required(login_url='/mrchampions/login')
def getVentaInfo(request):
    try:
        info=[]
        idventa = request.GET.get('idterminarventa','')
        venta = Venta.objects.get(id=idventa)
        info.append({
            'id':venta.id,
            'total':venta.total,
            'pagado':venta.pagado,
            'cambio':venta.cambio,
            'usuario':venta.usuario.first_name,
            'fecha_registro':venta.fecha_registro,
            'fecha_cancelado':venta.fecha_terminado,
            'fecha_terminado':venta.fecha_terminado,
            'estatus':venta.estatus,
            'motivo_cancelado':venta.motivo_cancelado
        })
        return JsonResponse({'info':info})
    except:
        return JsonResponse({})

@login_required(login_url='/mrchampions/login')
def ventas_agregar_producto(request):
    #try:
    idventa = request.GET['idventa']
    idproducto = request.GET['idproducto']
    cantidadprod =  request.GET['cantidadprod']
    venta = Venta.objects.get(id=idventa)
    producto = Producto.objects.get(id=idproducto)

    venta.total = venta.total + (producto.precio*float(cantidadprod))
    venta.save()
    detalleventa = DetalleVenta.objects.create()
    detalleventa.venta= venta
    detalleventa.producto=producto
    detalleventa.cantidad = cantidadprod
    detalleventa.precio_unitario = producto.precio
    detalleventa.subtotal = producto.precio*float(cantidadprod)
    detalleventa.save()
    resp = True    
    return JsonResponse({'resp':resp})
    #except:
    #    resp=False
    #    return JsonResponse({'resp':resp})

@login_required(login_url='/mrchampions/login')
def cuenta_cliente(request):
    data = []
    #try:
    idventa = request.GET['idventa']
    
    venta = Venta.objects.get(id=int(idventa))
    detalleventa = DetalleVenta.objects.filter(venta=venta)
    data2 = []
    for i in detalleventa:
        data2.append({
            'producto':str(i.producto.nombre),
            'cantidad':str(i.cantidad),
            'precio':str(i.subtotal),
        })
    data.append({
        'id':str(venta.id),
        'fecha':str(datetime.today()),
        'total':str(venta.total),
        'cliente':str(venta.cliente),
        'productos':data2
    })
    return JsonResponse({'data':data})
    #messages.error(request, 'Venta cancelada correctamente.', extra_tags='success')
    #return redirect('index')
    #except Exception as e:
    #    return JsonResponse({'data':'','venta':''})
        #messages.error(request, 'Error al cancelar venta: ' + str(e), extra_tags='danger')
        #return redirect('index')