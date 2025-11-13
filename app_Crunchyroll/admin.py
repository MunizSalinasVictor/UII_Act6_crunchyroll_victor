from django.contrib import admin
from .models import Empresa, Empleado, Venta, Suscripcion, Contenido, Usuario

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email_contacto', 'fecha_fundacion', 'pais_origen']
    list_filter = ['pais_origen', 'fecha_fundacion']
    search_fields = ['nombre', 'email_contacto']
    date_hierarchy = 'fecha_fundacion'

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'departamento', 'salario', 'activo', 'empresa']
    list_filter = ['departamento', 'activo', 'empresa', 'fecha_contratacion']
    search_fields = ['nombre', 'apellido', 'email']
    date_hierarchy = 'fecha_contratacion'

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['codigo_transaccion', 'monto', 'metodo_pago', 'estado', 'fecha_venta', 'usuario', 'suscripcion']
    list_filter = ['metodo_pago', 'estado', 'fecha_venta']
    search_fields = ['codigo_transaccion', 'usuario__nombre_usuario']
    date_hierarchy = 'fecha_venta'

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['nombre_plan', 'precio', 'calidad_video', 'num_dispositivos', 'descarga_offline', 'empresa']
    list_filter = ['descarga_offline', 'calidad_video', 'empresa']
    search_fields = ['nombre_plan']

@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'fecha_lanzamiento', 'categoria', 'suscripcion']
    list_filter = ['tipo', 'categoria', 'suscripcion']
    search_fields = ['titulo']
    date_hierarchy = 'fecha_lanzamiento'

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_usuario', 'email', 'fecha_registro', 'activo', 'suscripcion']
    list_filter = ['activo', 'suscripcion', 'fecha_registro']
    search_fields = ['nombre_usuario', 'email']