import os
import django
from datetime import date, datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_Crunchyroll.settings')
django.setup()

from app_Crunchyroll.models import Empresa, Empleado, Suscripcion, Contenido, Usuario, Venta

def insertar_datos_prueba():
    print("=== INSERTANDO DATOS DE PRUEBA ===")
    
    # Limpiar datos existentes (opcional)
    print("Limpiando datos existentes...")
    Venta.objects.all().delete()
    Usuario.objects.all().delete()
    Contenido.objects.all().delete()
    Empleado.objects.all().delete()
    Suscripcion.objects.all().delete()
    Empresa.objects.all().delete()
    
    # ==========================================
    # 1. INSERTAR EMPRESAS
    # ==========================================
    print("\n1. Insertando empresas...")
    
    empresas = [
        {
            'nombre': 'Crunchyroll LLC',
            'direccion': 'San Francisco, California, USA',
            'telefono': '+1-415-555-0101',
            'email_contacto': 'contact@crunchyroll.com',
            'fecha_fundacion': date(2006, 5, 1),
            'pais_origen': 'Estados Unidos'
        },
        {
            'nombre': 'Sony Pictures Entertainment',
            'direccion': 'Culver City, California, USA',
            'telefono': '+1-310-555-0202',
            'email_contacto': 'info@sonypictures.com',
            'fecha_fundacion': date(1987, 12, 21),
            'pais_origen': 'Estados Unidos'
        },
        {
            'nombre': 'Aniplex Inc.',
            'direccion': 'Tokyo, Japón',
            'telefono': '+81-3-5555-0303',
            'email_contacto': 'info@aniplex.co.jp',
            'fecha_fundacion': date(1995, 9, 1),
            'pais_origen': 'Japón'
        }
    ]
    
    empresas_creadas = []
    for emp_data in empresas:
        empresa = Empresa.objects.create(**emp_data)
        empresas_creadas.append(empresa)
        print(f"   ✅ Empresa creada: {empresa.nombre}")
    
    # ==========================================
    # 2. INSERTAR EMPLEADOS
    # ==========================================
    print("\n2. Insertando empleados...")
    
    empleados = [
        {
            'nombre': 'Ana',
            'apellido': 'García López',
            'email': 'ana.garcia@crunchyroll.com',
            'telefono': '+1-415-555-0101',
            'fecha_contratacion': date(2022, 3, 15),
            'salario': 45000.00,
            'departamento': 'soporte',
            'activo': True,
            'empresa': empresas_creadas[0]
        },
        {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez Martínez',
            'email': 'carlos.rodriguez@crunchyroll.com',
            'telefono': '+1-415-555-0102',
            'fecha_contratacion': date(2021, 7, 10),
            'salario': 52000.00,
            'departamento': 'tecnico',
            'activo': True,
            'empresa': empresas_creadas[0]
        },
        {
            'nombre': 'Laura',
            'apellido': 'Fernández Kim',
            'email': 'laura.fernandez@crunchyroll.com',
            'telefono': '+1-415-555-0103',
            'fecha_contratacion': date(2023, 1, 20),
            'salario': 38000.00,
            'departamento': 'contenido',
            'activo': True,
            'empresa': empresas_creadas[0]
        }
    ]
    
    empleados_creados = []
    for emp_data in empleados:
        empleado = Empleado.objects.create(**emp_data)
        empleados_creados.append(empleado)
        print(f"   ✅ Empleado creado: {empleado.nombre} {empleado.apellido}")
    
    # ==========================================
    # 3. INSERTAR SUSCRIPCIONES
    # ==========================================
    print("\n3. Insertando suscripciones...")
    
    suscripciones = [
        {
            'nombre_plan': 'Fan',
            'precio': 7.99,
            'calidad_video': '1080p',
            'num_dispositivos': 1,
            'beneficio_extra': 'Acceso a catálogo básico, sin anuncios',
            'descarga_offline': False,
            'empresa': empresas_creadas[0]
        },
        {
            'nombre_plan': 'Mega Fan',
            'precio': 9.99,
            'calidad_video': '1080p',
            'num_dispositivos': 4,
            'beneficio_extra': 'Acceso a catálogo completo, descargas offline, eventos exclusivos',
            'descarga_offline': True,
            'empresa': empresas_creadas[0]
        },
        {
            'nombre_plan': 'Ultimate Fan',
            'precio': 14.99,
            'calidad_video': '4K',
            'num_dispositivos': 6,
            'beneficio_extra': 'Máxima calidad, merch exclusivo, acceso prioritario',
            'descarga_offline': True,
            'empresa': empresas_creadas[0]
        }
    ]
    
    suscripciones_creadas = []
    for sub_data in suscripciones:
        suscripcion = Suscripcion.objects.create(**sub_data)
        suscripciones_creadas.append(suscripcion)
        print(f"   ✅ Suscripción creada: {suscripcion.nombre_plan} - ${suscripcion.precio}")
    
    # ==========================================
    # 4. INSERTAR CONTENIDO
    # ==========================================
    print("\n4. Insertando contenido...")
    
    contenidos = [
        {
            'titulo': 'Attack on Titan: The Final Season',
            'tipo': 'anime',
            'fecha_lanzamiento': date(2020, 12, 7),
            'categoria': 1,
            'capitulos': '16',
            'suscripcion': suscripciones_creadas[1]  # Mega Fan
        },
        {
            'titulo': 'Demon Slayer: Mugen Train',
            'tipo': 'pelicula',
            'fecha_lanzamiento': date(2020, 10, 16),
            'categoria': 1,
            'capitulos': '1',
            'suscripcion': suscripciones_creadas[2]  # Ultimate Fan
        },
        {
            'titulo': 'Jujutsu Kaisen',
            'tipo': 'anime',
            'fecha_lanzamiento': date(2020, 10, 3),
            'categoria': 1,
            'capitulos': '24',
            'suscripcion': suscripciones_creadas[0]  # Fan
        }
    ]
    
    contenidos_creados = []
    for cont_data in contenidos:
        contenido = Contenido.objects.create(**cont_data)
        contenidos_creados.append(contenido)
        print(f"   ✅ Contenido creado: {contenido.titulo}")
    
    # ==========================================
    # 5. INSERTAR USUARIOS
    # ==========================================
    print("\n5. Insertando usuarios...")
    
    usuarios = [
        {
            'nombre_usuario': 'akira_fan',
            'email': 'akira.tanaka@email.com',
            'password': 'password123',
            'activo': True,
            'suscripcion': suscripciones_creadas[2]  # Ultimate Fan
        },
        {
            'nombre_usuario': 'sakura_animelover',
            'email': 'sakura.yamamoto@email.com',
            'password': 'password123',
            'activo': True,
            'suscripcion': suscripciones_creadas[1]  # Mega Fan
        },
        {
            'nombre_usuario': 'kenji_otaku',
            'email': 'kenji.sato@email.com',
            'password': 'password123',
            'activo': False,  # Usuario inactivo
            'suscripcion': suscripciones_creadas[0]  # Fan
        }
    ]
    
    usuarios_creados = []
    for user_data in usuarios:
        usuario = Usuario.objects.create(**user_data)
        usuarios_creados.append(usuario)
        print(f"   ✅ Usuario creado: {usuario.nombre_usuario}")
    
    # ==========================================
    # 6. INSERTAR VENTAS
    # ==========================================
    print("\n6. Insertando ventas...")
    
    ventas = [
        {
            'monto': 14.99,
            'metodo_pago': 'tarjeta',
            'estado': 'completada',
            'codigo_transaccion': 'CR-TRX-001-2024',
            'usuario': usuarios_creados[0],
            'suscripcion': suscripciones_creadas[2],  # Ultimate Fan
            'empleado': empleados_creados[0]  # Ana García
        },
        {
            'monto': 9.99,
            'metodo_pago': 'paypal',
            'estado': 'completada',
            'codigo_transaccion': 'CR-TRX-002-2024',
            'usuario': usuarios_creados[1],
            'suscripcion': suscripciones_creadas[1],  # Mega Fan
            'empleado': empleados_creados[1]  # Carlos Rodríguez
        },
        {
            'monto': 7.99,
            'metodo_pago': 'transferencia',
            'estado': 'pendiente',
            'codigo_transaccion': 'CR-TRX-003-2024',
            'usuario': usuarios_creados[2],
            'suscripcion': suscripciones_creadas[0],  # Fan
            'empleado': None  # Sin empleado asignado
        }
    ]
    
    for venta_data in ventas:
        venta = Venta.objects.create(**venta_data)
        print(f"   ✅ Venta creada: {venta.codigo_transaccion} - ${venta.monto}")
    
    # ==========================================
    # RESUMEN FINAL
    # ==========================================
    print("\n" + "="*50)
    print("✅ DATOS DE PRUEBA INSERTADOS EXITOSAMENTE")
    print("="*50)
    print(f"📊 Empresas: {Empresa.objects.count()}")
    print(f"👥 Empleados: {Empleado.objects.count()}")
    print(f"💳 Suscripciones: {Suscripcion.objects.count()}")
    print(f"🎬 Contenido: {Contenido.objects.count()}")
    print(f"👤 Usuarios: {Usuario.objects.count()}")
    print(f"💰 Ventas: {Venta.objects.count()}")
    print("="*50)
    print("\n🎯 Ahora puedes acceder a todas las secciones:")
    print("   http://127.0.0.1:8000/empresas/ver/")
    print("   http://127.0.0.1:8000/empleados/ver/")
    print("   http://127.0.0.1:8000/ventas/ver/")
    print("   http://127.0.0.1:8000/suscripciones/ver/")
    print("   http://127.0.0.1:8000/contenido/ver/")
    print("   http://127.0.0.1:8000/usuarios/ver/")

if __name__ == '__main__':
    insertar_datos_prueba()