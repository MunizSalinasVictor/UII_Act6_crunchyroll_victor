from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_crunchyroll, name='inicio_crunchyroll'),
    
    # URLs para Empresas
    path('empresas/agregar/', views.agregar_empresa, name='agregar_empresa'),
    path('empresas/ver/', views.ver_empresas, name='ver_empresas'),
    path('empresas/actualizar/<int:id>/', views.actualizar_empresa, name='actualizar_empresa'),
    path('empresas/borrar/<int:id>/', views.borrar_empresa, name='borrar_empresa'),
    
    # URLs para Empleados
    path('empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleados/ver/', views.ver_empleados, name='ver_empleados'),
    path('empleados/actualizar/<int:id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/borrar/<int:id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # URLs para Ventas
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/ver/', views.ver_ventas, name='ver_ventas'),
    path('ventas/actualizar/<int:id>/', views.actualizar_venta, name='actualizar_venta'),
    path('ventas/borrar/<int:id>/', views.borrar_venta, name='borrar_venta'),
    
    # URLs para Suscripciones (existentes)
    path('suscripciones/agregar/', views.agregar_Suscripcion, name='agregar_Suscripcion'),
    path('suscripciones/ver/', views.ver_Suscripciones, name='ver_Suscripciones'),
    path('suscripciones/actualizar/<int:id>/', views.actualizar_Suscripcion, name='actualizar_Suscripcion'),
    path('suscripciones/borrar/<int:id>/', views.borrar_Suscripcion, name='borrar_Suscripcion'),
    
    # URLs para Contenido (existentes)
    path('contenido/agregar/', views.agregar_contenido, name='agregar_contenido'),
    path('contenido/ver/', views.ver_contenido, name='ver_contenido'),
    path('contenido/actualizar/<int:id>/', views.actualizar_contenido, name='actualizar_contenido'),
    path('contenido/borrar/<int:id>/', views.borrar_contenido, name='borrar_contenido'),
    
    # URLs para Usuarios (existentes)
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/ver/', views.ver_usuarios, name='ver_usuarios'),
    path('usuarios/actualizar/<int:id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/borrar/<int:id>/', views.borrar_usuario, name='borrar_usuario'),
]