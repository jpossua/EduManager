"""
======================================================================
MANAGE.PY - Punto de entrada principal de Django
======================================================================
Este archivo es la herramienta de línea de comandos de Django.
Se usa para ejecutar comandos como:
  - python manage.py runserver   → Inicia el servidor de desarrollo
  - python manage.py migrate     → Aplica las migraciones a la BD
  - python manage.py makemigrations → Genera archivos de migración
  - python manage.py createsuperuser → Crea un usuario administrador

IMPORTANTE: La variable DJANGO_SETTINGS_MODULE le dice a Django
dónde está el archivo de configuración del proyecto (settings.py).
Si renombraste la carpeta del proyecto, DEBES actualizar esta línea.
======================================================================
"""

#!/usr/bin/env python
import os
import sys


def main():
    """Función principal que ejecuta las tareas administrativas de Django."""

    # Indicamos a Django dónde encontrar la configuración del proyecto.
    # 'EduManager.settings' significa: carpeta EduManager → archivo settings.py
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduManager.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado "
            "y disponible en tu PYTHONPATH? ¿Olvidaste activar el entorno virtual?"
        ) from exc

    # Ejecuta el comando que el usuario escribió en la terminal
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
