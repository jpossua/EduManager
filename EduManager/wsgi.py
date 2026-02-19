"""
======================================================================
WSGI.PY - Configuración para despliegue en producción (WSGI)
======================================================================
WSGI = Web Server Gateway Interface (Interfaz de Pasarela del Servidor Web)

Este archivo es el punto de entrada cuando despliegas tu aplicación
en un servidor de producción como Apache, Nginx + Gunicorn, etc.

¿Cuándo se usa?
  - En PRODUCCIÓN: El servidor web (Apache/Nginx) usa este archivo
    para comunicarse con tu aplicación Django.
  - En DESARROLLO: No se usa directamente; Django usa su propio
    servidor con "python manage.py runserver".

IMPORTANTE: Si renombraste la carpeta del proyecto, actualiza
DJANGO_SETTINGS_MODULE con el nuevo nombre.
======================================================================
"""

import os

from django.core.wsgi import get_wsgi_application

# Le decimos a Django dónde está nuestro settings.py
# 'EduManager.settings' → carpeta EduManager → archivo settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduManager.settings")

# Creamos la aplicación WSGI que el servidor web utilizará
application = get_wsgi_application()
