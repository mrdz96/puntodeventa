from . import views
from . import datatables
from django.urls import path,re_path
from .views import permission_required_2

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('permiso/visualizacion',(views.get_permiso_visualizacion), name='get_permiso_visualizacion'),
    
    #EMPLEADOS
    path('usuarios/lista', permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (views.usuarios_lista), name='usuarios_lista'),
    path('usuarios/insertar/', permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (views.usuarios_insertar), name='usuarios_insertar'),
    path('usuarios/insertar/save', permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (views.usuarios_insertar_save), name='usuarios_insertar_save'),
    re_path(r'^usuarios/editar/(?P<id>\d+)$', permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (views.usuarios_editar), name='usuarios_editar'),
    path('usuarios/editar/save', permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (views.usuarios_editar_save), name='usuarios_editar_save'),
    path('usuarios/eliminar', permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (views.usuarios_eliminar), name='usuarios_eliminar'),
    path('DTUsuarios',permission_required_2('system.usuarios-lista', login_url='/mrchampions/login') (datatables.DTUsuarios.as_view()), name='DTUsuarios'),
    
    #PUESTOS
    path('puestos/lista', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.puestos_lista), name='puestos_lista'),
    path('puestos/insertar/', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.puestos_insertar), name='puestos_insertar'),
    path('puestos/insertar/save', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.puestos_insertar_save), name='puestos_insertar_save'),
    re_path(r'^puestos/editar/(?P<id>\d+)$', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.puestos_editar), name='puestos_editar'),
    path('puestos/editar/save', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.puestos_editar_save), name='puestos_editar_save'),
    path('puestos/eliminar', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.puestos_eliminar), name='puestos_eliminar'),
    path('DTPuestos',permission_required_2('system.puesto-lista', login_url='/mrchampions/login') (datatables.DTPuestos.as_view()), name='DTPuestos'),
    
    #PRODUCTOS
    path('productos/lista', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_lista), name='productos_lista'),
    path('productos/insertar', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_insertar), name='productos_insertar'),
    path('productos/insertar/save', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_insertar_save), name='productos_insertar_save'),
    re_path(r'^productos/editar/(?P<id>\d+)$', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_editar), name='productos_editar'),
    path('productos/editar/save', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_editar_save), name='productos_editar_save'),
    path('DTProductos',permission_required_2('system.puesto-lista', login_url='/mrchampions/login') (datatables.DTProductos.as_view()), name='DTProductos'),
    re_path(r'^productos/editar/(?P<id>\d+)$', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_editar), name='productos_editar'),
    path('productos/eliminar', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.productos_eliminar), name='productos_eliminar'),
    
    #CATEGOIRA PRODUCTOS
    path('categoiraproductos/lista', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.categoria_productos_lista), name='categoria_productos_lista'),
    path('categoiraproductos/insertar', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.categoria_productos_insertar), name='categoria_productos_insertar'),
    path('categoiraproductos/insertar/save', permission_required_2('system.puestos-lista', login_url='/mrchampions/login') (views.categoria_productos_insertar_save), name='categoria_productos_insertar_save'),
    path('DTCategoriaProductos',permission_required_2('system.puesto-lista', login_url='/mrchampions/login') (datatables.DTCategoriaProductos.as_view()), name='DTCategoriaProductos'),

    #VENTAS
    path('ventas/lista', permission_required_2('system.ventas-lista', login_url='/mrchampions/login') (views.ventas_lista), name='ventas_lista'),
    path('ventas/insertar',  (views.ventas_insertar), name='ventas_insertar'),
    path('ventas/ventas_registrar_save',  (views.ventas_registrar_save), name='ventas_registrar_save'),
    path('ventas_cancelar_save',  (views.ventas_cancelar_save), name='ventas_cancelar_save'),
    path('ventas_terminar_save', (views.ventas_terminar_save), name='ventas_terminar_save'),
    
    path('DTVentas',permission_required_2('system.ventas-lista', login_url='/mrchampions/login') (datatables.DTVentas.as_view()), name='DTVentas'),
    path('DTVentasRegistradas', (datatables.DTVentasRegistradas.as_view()), name='DTVentasRegistradas'),
    path('DTVentasTerminadas', (datatables.DTVentasTerminadas.as_view()), name='DTVentasTerminadas'),
    path('DTVentasCanceladas', (datatables.DTVentasCanceladas.as_view()), name='DTVentasCanceladas'),
    path('DTMenu', (datatables.DTMenu.as_view()), name='DTMenu'),
    
    re_path(r'^ventas/info/(?P<id>\d+)$',  (views.ventas_info), name='ventas_info'),
    path('getProductoInfo', (views.getProductoInfo), name='getProductoInfo'),
    path('getVentaInfo',(views.getVentaInfo), name='getVentaInfo'),
    path('ventas_agregar_producto',(views.ventas_agregar_producto), name='ventas_agregar_producto'),
    path('cuenta_cliente',(views.cuenta_cliente),name='cuenta_cliente'),
    
]

