"""
======================================================================
MODELS.PY - Modelos de datos (Tablas en la Base de Datos)
======================================================================
En Django, cada clase que hereda de models.Model se convierte en una
tabla en la base de datos. Cada atributo de la clase es una columna.

Nuestro esquema de base de datos:
  ┌──────────┐     ┌──────────┐     ┌────────────┐     ┌────────┐
  │  User    │────▶│  Materia │◀────│  Actividad │◀────│  Nota  │
  │(Profesor)│     │          │     │(Examen,etc)│     │(0-10)  │
  └──────────┘     └──────────┘     └────────────┘     └────────┘
                        ▲                                   │
                        │          ┌──────────┐             │
                        └──────────│  Alumno  │◀────────────┘
                      (M2M)       └──────────┘

Relaciones:
  - User → Materia:     Un profesor tiene MUCHAS materias (ForeignKey)
  - Alumno ↔ Materia:   Muchos alumnos en muchas materias (ManyToMany)
  - Materia → Actividad: Una materia tiene MUCHAS actividades (ForeignKey)
  - Alumno + Actividad → Nota: Cada nota vincula un alumno con una actividad

Comandos para aplicar cambios en los modelos:
  python manage.py makemigrations  → Genera el archivo de migración
  python manage.py migrate         → Ejecuta la migración en la BD
======================================================================
"""

from django.db import models
from django.contrib.auth.models import User  # Modelo de usuario de Django (profesor)
from django.core.exceptions import ValidationError  # Para validaciones personalizadas


# =====================================================================
# 1. MODELO: MATERIA
# =====================================================================
# Representa una asignatura (Matemáticas, Física, etc.)
# Cada materia PERTENECE a un profesor (relación uno-a-muchos).
# Esto permite que cada profesor solo vea SUS propias materias.
class Materia(models.Model):
    # CharField: Campo de texto con límite de caracteres
    nombre = models.CharField(max_length=100)

    # ForeignKey: Relación muchos-a-uno con User (profesor)
    # on_delete=CASCADE: Si se elimina el profesor, se eliminan sus materias
    # Otras opciones: PROTECT (impide borrar), SET_NULL (pone null)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Representación en texto del objeto.
        Se muestra en el panel admin, selects de formularios, y en print().
        Ejemplo: "Matemáticas I"
        """
        return self.nombre


# =====================================================================
# 2. MODELO: ALUMNO
# =====================================================================
# Representa a un estudiante.
# Un alumno puede estar inscrito en VARIAS materias (relación M2M).
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)

    # EmailField: Campo de texto que valida formato de email
    # unique=True: No se permiten dos alumnos con el mismo correo
    correo = models.EmailField(unique=True)

    # ManyToManyField: Relación muchos-a-muchos con Materia
    # Django crea automáticamente una tabla intermedia (alumno_materias)
    # Un alumno puede estar en varias materias, y una materia puede
    # tener varios alumnos.
    materias = models.ManyToManyField(Materia)

    def __str__(self):
        return self.nombre


# =====================================================================
# 3. MODELO: ACTIVIDAD
# =====================================================================
# Representa una tarea evaluable: examen, trabajo, práctica, etc.
# Cada actividad pertenece a UNA materia (ForeignKey).
class Actividad(models.Model):
    # CATEGORIAS: Lista de tuplas para el campo 'choices'.
    # El primer valor ('EX') se guarda en la BD (máximo 2 caracteres).
    # El segundo valor ('Examen') se muestra al usuario en formularios.
    CATEGORIAS = [
        ("EX", "Examen"),
        ("TR", "Trabajo"),
        ("PR", "Practica"),
        ("OT", "Otro"),
    ]

    # Relación con Materia: Si se elimina la materia, se eliminan sus actividades
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=100)

    # choices=CATEGORIAS: Limita las opciones a la lista definida arriba
    # En la BD se guarda 'EX', pero en el formulario se muestra 'Examen'
    categoria = models.CharField(max_length=2, choices=CATEGORIAS)

    # DateField: Campo de fecha (año-mes-día)
    fecha = models.DateField()

    def __str__(self):
        # f-string: Forma moderna de formatear texto en Python
        return f"{self.nombre} - {self.materia}"


# =====================================================================
# 4. MODELO: NOTA
# =====================================================================
# Representa la calificación de un alumno en una actividad.
# Es el modelo central que conecta Alumno ↔ Actividad.
class Nota(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    # DecimalField: Número decimal con precisión controlada
    # max_digits=5: máximo 5 dígitos en total (ej: 999.99)
    # decimal_places=2: 2 decimales (ej: 8.75)
    nota = models.DecimalField(max_digits=5, decimal_places=2)

    # -----------------------------------------------------------------
    # REGLAS DE NEGOCIO (Validaciones personalizadas)
    # -----------------------------------------------------------------
    # 1. La nota debe estar entre 0 y 10
    # 2. Un alumno NO puede tener dos notas en la misma actividad
    #    (esto se controla con unique_together en Meta)

    def clean(self):
        """
        Método de validación personalizada.
        Django lo llama automáticamente en formularios (form.is_valid()).
        También lo llamamos manualmente en save() por seguridad.
        """
        if self.nota < 0 or self.nota > 10:
            raise ValidationError("La nota debe estar entre 0 y 10")

    def save(self, *args, **kwargs):
        """
        Sobreescribimos el método save() para forzar la validación
        ANTES de guardar en la BD. Esto protege contra inserciones
        directas que no pasen por un formulario.
        """
        self.clean()  # Ejecutamos la validación
        super().save(*args, **kwargs)  # Llamamos al save() original de Django

    class Meta:
        """
        Clase Meta: Configuración adicional del modelo.
        unique_together: Garantiza que NO existan dos registros
        con la misma combinación de alumno + actividad.
        Así evitamos que un alumno tenga dos notas en el mismo examen.
        """

        unique_together = ("alumno", "actividad")

    def __str__(self):
        return f"{self.alumno} - {self.actividad} - {self.nota}"
