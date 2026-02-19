"""
======================================================================
ASGI.PY - Configuración para despliegue asíncrono (ASGI)
======================================================================
ASGI = Asynchronous Server Gateway Interface

Similar a WSGI pero soporta comunicación asíncrona:
  - WebSockets (chat en tiempo real)
  - Conexiones de larga duración
  - Eventos en tiempo real

En este proyecto no usamos funciones asíncronas, pero Django
lo incluye por defecto desde la versión 3.0 para futura compatibilidad.

IMPORTANTE: Si renombraste la carpeta del proyecto, actualiza
DJANGO_SETTINGS_MODULE con el nuevo nombre.
======================================================================
"""

import os

from django.core.asgi import get_asgi_application

# Le decimos a Django dónde está nuestro settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduManager.settings")

# Creamos la aplicación ASGI
application = get_asgi_application()
