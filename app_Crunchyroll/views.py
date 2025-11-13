from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Avg, Sum
from .models import Suscripcion, Contenido, Usuario, Empresa, Empleado, Venta
from django.utils.dateparse import parse_date

def inicio_crunchyroll(request):
    return render(request, 'inicio.html')

# ==========================================
# VISTAS PARA SUSCRIPCIONES
# ==========================================

def agregar_Suscripcion(request):
    empresas = Empresa.objects.all()
    if request.method == 'POST':
        Suscripcion.objects.create(
            nombre_plan=request.POST['nombre_plan'],
            precio=request.POST['precio'],
            calidad_video=request.POST['calidad_video'],
            num_dispositivos=request.POST['num_dispositivos'],
            beneficio_extra=request.POST['beneficio_extra'],
            descarga_offline='descarga_offline' in request.POST,
            empresa_id=request.POST['empresa']
        )
        return redirect('ver_Suscripciones')
    return render(request, 'suscripciones/agregar_Suscripciones.html', {'empresas': empresas})

def ver_Suscripciones(request):
    suscripciones = Suscripcion.objects.all().select_related('empresa')
    
    # Estadísticas para suscripciones
    suscripciones_con_descarga = suscripciones.filter(descarga_offline=True).count()
    empresas_count = Empresa.objects.count()
    
    # Calcular precio promedio
    if suscripciones.exists():
        precio_promedio = round(suscripciones.aggregate(avg_precio=Avg('precio'))['avg_precio'], 2)
    else:
        precio_promedio = 0
    
    return render(request, 'suscripciones/ver_Suscripciones.html', {
        'suscripciones': suscripciones,
        'suscripciones_con_descarga': suscripciones_con_descarga,
        'empresas_count': empresas_count,
        'precio_promedio': precio_promedio,
    })

def actualizar_Suscripcion(request, id):
    suscripcion = get_object_or_404(Suscripcion, id=id)
    empresas = Empresa.objects.all()
    
    if request.method == 'POST':
        suscripcion.nombre_plan = request.POST['nombre_plan']
        suscripcion.precio = request.POST['precio']
        suscripcion.calidad_video = request.POST['calidad_video']
        suscripcion.num_dispositivos = request.POST['num_dispositivos']
        suscripcion.beneficio_extra = request.POST['beneficio_extra']
        suscripcion.descarga_offline = 'descarga_offline' in request.POST
        suscripcion.empresa_id = request.POST['empresa']
        suscripcion.save()
        return redirect('ver_Suscripciones')
    
    return render(request, 'suscripciones/actualizar_Suscripciones.html', {
        'suscripcion': suscripcion,
        'empresas': empresas
    })

def borrar_Suscripcion(request, id):
    suscripcion = get_object_or_404(Suscripcion, id=id)
    
    if request.method == 'POST':
        suscripcion.delete()
        return redirect('ver_Suscripciones')
    
    return render(request, 'suscripciones/borrar_Suscripcion.html', {'suscripcion': suscripcion})

# ==========================================
# VISTAS PARA CONTENIDO
# ==========================================

def agregar_contenido(request):
    suscripciones = Suscripcion.objects.all()
    
    if request.method == 'POST':
        Contenido.objects.create(
            titulo=request.POST['titulo'],
            tipo=request.POST['tipo'],
            fecha_lanzamiento=request.POST['fecha_lanzamiento'],
            categoria=request.POST['categoria'],
            capitulos=request.POST['capitulos'],
            suscripcion_id=request.POST['suscripcion']
        )
        return redirect('ver_contenido')
    
    return render(request, 'contenido/agregar_contenido.html', {'suscripciones': suscripciones})

def ver_contenido(request):
    contenidos = Contenido.objects.all().select_related('suscripcion')
    
    # Estadísticas para contenido (actualizadas)
    anime_count = contenidos.filter(tipo='anime').count()
    peliculas_count = contenidos.filter(tipo='pelicula').count()
    manga_count = contenidos.filter(tipo='manga').count()
    
    # Conteo por categoría
    categorias_count = contenidos.values('categoria').annotate(total=Count('id'))
    
    return render(request, 'contenido/ver_contenido.html', {
        'contenidos': contenidos,
        'anime_count': anime_count,
        'peliculas_count': peliculas_count,
        'manga_count': manga_count,
        'categorias_count': categorias_count,
    })

def actualizar_contenido(request, id):
    contenido = get_object_or_404(Contenido, id=id)
    suscripciones = Suscripcion.objects.all()
    
    if request.method == 'POST':
        contenido.titulo = request.POST['titulo']
        contenido.tipo = request.POST['tipo']
        contenido.fecha_lanzamiento = request.POST['fecha_lanzamiento']
        contenido.categoria = request.POST['categoria']
        contenido.capitulos = request.POST['capitulos']
        contenido.suscripcion_id = request.POST['suscripcion']
        contenido.save()
        return redirect('ver_contenido')
    
    return render(request, 'contenido/actualizar_contenido.html', {
        'contenido': contenido,
        'suscripciones': suscripciones
    })

def borrar_contenido(request, id):
    contenido = get_object_or_404(Contenido, id=id)
    
    if request.method == 'POST':
        contenido.delete()
        return redirect('ver_contenido')
    
    return render(request, 'contenido/borrar_contenido.html', {'contenido': contenido})

# ==========================================
# VISTAS PARA USUARIOS
# ==========================================

def agregar_usuario(request):
    suscripciones = Suscripcion.objects.all()
    
    if request.method == 'POST':
        Usuario.objects.create(
            nombre_usuario=request.POST['nombre_usuario'],
            email=request.POST['email'],
            password=request.POST['password'],
            activo='activo' in request.POST,
            suscripcion_id=request.POST['suscripcion']
        )
        return redirect('ver_usuarios')
    
    return render(request, 'usuarios/agregar_usuario.html', {'suscripciones': suscripciones})

def ver_usuarios(request):
    usuarios = Usuario.objects.all().select_related('suscripcion')
    
    # Estadísticas para usuarios
    usuarios_activos = usuarios.filter(activo=True).count()
    usuarios_inactivos = usuarios.filter(activo=False).count()
    suscripciones_count = Suscripcion.objects.count()
    
    # Usuarios por suscripción
    usuarios_por_suscripcion = usuarios.values('suscripcion__nombre_plan').annotate(total=Count('id'))
    
    return render(request, 'usuarios/ver_usuarios.html', {
        'usuarios': usuarios,
        'usuarios_activos': usuarios_activos,
        'usuarios_inactivos': usuarios_inactivos,
        'suscripciones_count': suscripciones_count,
        'usuarios_por_suscripcion': usuarios_por_suscripcion,
    })

def actualizar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    suscripciones = Suscripcion.objects.all()
    
    if request.method == 'POST':
        usuario.nombre_usuario = request.POST['nombre_usuario']
        usuario.email = request.POST['email']
        usuario.password = request.POST['password']
        usuario.activo = 'activo' in request.POST
        usuario.suscripcion_id = request.POST['suscripcion']
        usuario.save()
        return redirect('ver_usuarios')
    
    return render(request, 'usuarios/actualizar_usuario.html', {
        'usuario': usuario,
        'suscripciones': suscripciones
    })

def borrar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        usuario.delete()
        return redirect('ver_usuarios')
    
    return render(request, 'usuarios/borrar_usuario.html', {'usuario': usuario})

# ==========================================
# VISTAS PARA EMPRESA
# ==========================================

def agregar_empresa(request):
    if request.method == 'POST':
        Empresa.objects.create(
            nombre=request.POST['nombre'],
            direccion=request.POST['direccion'],
            telefono=request.POST['telefono'],
            email_contacto=request.POST['email_contacto'],
            fecha_fundacion=request.POST['fecha_fundacion'],
            pais_origen=request.POST['pais_origen']
        )
        return redirect('ver_empresas')
    return render(request, 'empresas/agregar_empresa.html')

def ver_empresas(request):
    empresas = Empresa.objects.all()
    
    # Estadísticas para empresas
    empleados_count = Empleado.objects.count()
    suscripciones_count = Suscripcion.objects.count()
    paises_count = empresas.values('pais_origen').distinct().count()
    
    return render(request, 'empresas/ver_empresas.html', {
        'empresas': empresas,
        'empleados_count': empleados_count,
        'suscripciones_count': suscripciones_count,
        'paises_count': paises_count,
    })

def actualizar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    if request.method == 'POST':
        empresa.nombre = request.POST['nombre']
        empresa.direccion = request.POST['direccion']
        empresa.telefono = request.POST['telefono']
        empresa.email_contacto = request.POST['email_contacto']
        empresa.fecha_fundacion = request.POST['fecha_fundacion']
        empresa.pais_origen = request.POST['pais_origen']
        empresa.save()
        return redirect('ver_empresas')
    return render(request, 'empresas/actualizar_empresa.html', {'empresa': empresa})

def borrar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    if request.method == 'POST':
        empresa.delete()
        return redirect('ver_empresas')
    return render(request, 'empresas/borrar_empresa.html', {'empresa': empresa})

# ==========================================
# VISTAS PARA EMPLEADO
# ==========================================

def agregar_empleado(request):
    empresas = Empresa.objects.all()
    if request.method == 'POST':
        Empleado.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            email=request.POST['email'],
            telefono=request.POST['telefono'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario'],
            departamento=request.POST['departamento'],
            activo='activo' in request.POST,
            empresa_id=request.POST['empresa']
        )
        return redirect('ver_empleados')
    return render(request, 'empleados/agregar_empleado.html', {'empresas': empresas})

def ver_empleados(request):
    empleados = Empleado.objects.all().select_related('empresa')
    
    # Estadísticas para empleados
    empleados_activos = empleados.filter(activo=True).count()
    empleados_inactivos = empleados.filter(activo=False).count()
    empresas_count = Empresa.objects.count()
    
    # Empleados por departamento
    empleados_por_departamento = empleados.values('departamento').annotate(total=Count('id'))
    
    # Salario promedio
    if empleados.exists():
        salario_promedio = round(empleados.aggregate(avg_salario=Avg('salario'))['avg_salario'], 2)
    else:
        salario_promedio = 0
    
    return render(request, 'empleados/ver_empleados.html', {
        'empleados': empleados,
        'empleados_activos': empleados_activos,
        'empleados_inactivos': empleados_inactivos,
        'empresas_count': empresas_count,
        'salario_promedio': salario_promedio,
        'empleados_por_departamento': empleados_por_departamento,
    })

def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empresas = Empresa.objects.all()
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.email = request.POST['email']
        empleado.telefono = request.POST['telefono']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.departamento = request.POST['departamento']
        empleado.activo = 'activo' in request.POST
        empleado.empresa_id = request.POST['empresa']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'empleados/actualizar_empleado.html', {
        'empleado': empleado,
        'empresas': empresas
    })

def borrar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleados/borrar_empleado.html', {'empleado': empleado})

# ==========================================
# VISTAS PARA VENTA
# ==========================================

def agregar_venta(request):
    usuarios = Usuario.objects.all()
    suscripciones = Suscripcion.objects.all()
    empleados = Empleado.objects.all()
    
    if request.method == 'POST':
        Venta.objects.create(
            monto=request.POST['monto'],
            metodo_pago=request.POST['metodo_pago'],
            estado=request.POST['estado'],
            codigo_transaccion=request.POST['codigo_transaccion'],
            usuario_id=request.POST['usuario'],
            suscripcion_id=request.POST['suscripcion'],
            empleado_id=request.POST['empleado'] if request.POST['empleado'] else None
        )
        return redirect('ver_ventas')
    
    return render(request, 'ventas/agregar_venta.html', {
        'usuarios': usuarios,
        'suscripciones': suscripciones,
        'empleados': empleados
    })

def ver_ventas(request):
    ventas = Venta.objects.all().select_related('usuario', 'suscripcion', 'empleado')
    
    # Estadísticas para ventas
    ventas_count = ventas.count()
    ventas_completadas = ventas.filter(estado='completada').count()
    ventas_pendientes = ventas.filter(estado='pendiente').count()
    ventas_canceladas = ventas.filter(estado='cancelada').count()
    
    # Total de ingresos (solo ventas completadas)
    total_ventas = round(ventas.filter(estado='completada').aggregate(total=Sum('monto'))['total'] or 0, 2)
    
    # Usuarios activos
    usuarios_count = Usuario.objects.filter(activo=True).count()
    
    # Ventas por método de pago
    ventas_por_metodo = ventas.values('metodo_pago').annotate(total=Count('id'))
    
    return render(request, 'ventas/ver_ventas.html', {
        'ventas': ventas,
        'ventas_count': ventas_count,
        'ventas_completadas': ventas_completadas,
        'ventas_pendientes': ventas_pendientes,
        'ventas_canceladas': ventas_canceladas,
        'total_ventas': total_ventas,
        'usuarios_count': usuarios_count,
        'ventas_por_metodo': ventas_por_metodo,
    })

def actualizar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    usuarios = Usuario.objects.all()
    suscripciones = Suscripcion.objects.all()
    empleados = Empleado.objects.all()
    
    if request.method == 'POST':
        venta.monto = request.POST['monto']
        venta.metodo_pago = request.POST['metodo_pago']
        venta.estado = request.POST['estado']
        venta.codigo_transaccion = request.POST['codigo_transaccion']
        venta.usuario_id = request.POST['usuario']
        venta.suscripcion_id = request.POST['suscripcion']
        venta.empleado_id = request.POST['empleado'] if request.POST['empleado'] else None
        venta.save()
        return redirect('ver_ventas')
    
    return render(request, 'ventas/actualizar_venta.html', {
        'venta': venta,
        'usuarios': usuarios,
        'suscripciones': suscripciones,
        'empleados': empleados
    })

def borrar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    return render(request, 'ventas/borrar_venta.html', {'venta': venta})