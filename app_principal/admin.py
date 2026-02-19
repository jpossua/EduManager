"""
======================================================================
ADMIN.PY - Configuración del Panel de Administración de Django
======================================================================
El panel admin (/admin/) es una herramienta integrada de Django que
permite gestionar los datos de la BD desde una interfaz web.

Para acceder necesitas un superusuario:
  python manage.py createsuperuser

admin.site.register(Modelo) → Registra un modelo para que aparezca
en el panel admin. Sin esto, el modelo existe en la BD pero NO se
ve en el panel.

NOTA: El panel admin es para ADMINISTRADORES del sistema, no para
los profesores. Los profesores usan nuestra interfaz personalizada.
======================================================================
"""

from django.contrib import admin
from .models import Materia, Alumno, Actividad, Nota

# Registramos cada modelo para que sea visible en /admin/
# Esto permite a los administradores ver, crear, editar y eliminar
# registros directamente desde el panel de administración.
admin.site.register(Materia)  # Gestión de materias
admin.site.register(Alumno)  # Gestión de alumnos
admin.site.register(Actividad)  # Gestión de actividades
admin.site.register(Nota)  # Gestión de calificaciones
