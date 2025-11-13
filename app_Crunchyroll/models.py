from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ==========================================
# MODELO: EMPRESA
# ==========================================
class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    fecha_fundacion = models.DateField()
    pais_origen = models.CharField(max_length=50, default='Japón')
    
    class Meta:
        db_table = 'empresa'
    
    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: EMPLEADO
# ==========================================
class Empleado(models.Model):
    DEPARTAMENTO_CHOICES = [
        ('soporte', 'Soporte al Cliente'),
        ('tecnico', 'Técnico'),
        ('contenido', 'Gestión de Contenido'),
        ('marketing', 'Marketing'),
        ('administracion', 'Administración'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTO_CHOICES)
    activo = models.BooleanField(default=True)
    
    # Relación con Empresa
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='empleados'
    )
    
    class Meta:
        db_table = 'empleado'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.departamento}"

# ==========================================
# MODELO: VENTA
# ==========================================
class Venta(models.Model):
    ESTADO_CHOICES = [
        ('completada', 'Completada'),
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
        ('reembolsada', 'Reembolsada'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('paypal', 'PayPal'),
        ('transferencia', 'Transferencia Bancaria'),
        ('crypto', 'Criptomoneda'),
    ]
    
    fecha_venta = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='completada')
    codigo_transaccion = models.CharField(max_length=100, unique=True)
    
    # Relaciones
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    suscripcion = models.ForeignKey(
        'Suscripcion',
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas_gestionadas'
    )
    
    class Meta:
        db_table = 'venta'
    
    def __str__(self):
        return f"Venta {self.codigo_transaccion} - ${self.monto}"

# ==========================================
# MODELO: SUSCRIPCIÓN (Actualizado)
# ==========================================
class Suscripcion(models.Model):
    nombre_plan = models.CharField(max_length=50, unique=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    calidad_video = models.CharField(max_length=20)
    num_dispositivos = models.IntegerField()
    beneficio_extra = models.TextField()
    descarga_offline = models.BooleanField(default=False)
    
    # Relación con Empresa
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='suscripciones'
    )
    
    # Relación muchos a muchos: una suscripción puede tener varios contenidos exclusivos
    contenidos_exclusivos = models.ManyToManyField(
        'Contenido', 
        related_name='suscripciones_exclusivas',
        blank=True
    )
    # Relación muchos a muchos: una suscripción puede tener varios usuarios premium
    usuarios_premium = models.ManyToManyField(
        'Usuario', 
        related_name='suscripciones_adicionales',
        blank=True
    )

    class Meta:
        db_table = 'suscripcion'
    
    def __str__(self):
        return f"{self.nombre_plan} - ${self.precio}"

# ==========================================
# MODELO: CONTENIDO 
# ==========================================
class Contenido(models.Model):
    TIPO_CHOICES = [
        ('anime', 'Anime'),
        ('pelicula', 'Película'),
        ('manga', 'Manga'),
    ]
    
    titulo = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_lanzamiento = models.DateField()
    categoria = models.IntegerField()
    capitulos = models.CharField(max_length=5)
    
    # Relación 1 a muchos: una suscripción puede tener varios contenidos principales
    suscripcion = models.ForeignKey(
        Suscripcion, 
        on_delete=models.CASCADE,
        related_name='contenidos_principales'
    )

    class Meta:
        db_table = 'contenido'
    
    def __str__(self):
        return self.titulo
    
    def get_categoria_display(self):
        categorias = {
            1: 'Shonen', 2: 'Shojo', 3: 'Seinen', 4: 'Josei', 5: 'Kodomo',
            6: 'Mecha', 7: 'Isekai', 8: 'Fantasia', 9: 'Ciencia Ficción',
            10: 'Romance', 11: 'Comedia', 12: 'Terror', 13: 'Drama',
            14: 'Aventura', 15: 'Acción'
        }
        return categorias.get(self.categoria, 'Desconocida')


# ==========================================
# MODELO: USUARIO
# ==========================================
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    fecha_registro = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    # Relación 1 a muchos: una suscripción puede tener varios usuarios principales
    suscripcion = models.ForeignKey(
        Suscripcion, 
        on_delete=models.CASCADE,
        related_name='usuarios_principales'
    )

    class Meta:
        db_table = 'usuario'
    
    def __str__(self):
        return self.nombre_usuario
