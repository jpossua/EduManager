"""
======================================================================
URLS.PY (Proyecto) - Enrutador principal del proyecto EduManager
======================================================================
Este archivo es el "mapa de rutas" principal. Cuando un usuario
visita una URL, Django busca aquí qué vista debe ejecutar.

Estructura de URLs del proyecto:
  /admin/      → Panel de administración de Django
  /accounts/   → URLs de autenticación de Django (login, logout, etc.)
  /            → Todas las URLs de nuestra app (app_principal/urls.py)

La función include() permite DELEGAR las URLs de cada app
a su propio archivo urls.py, manteniendo el código organizado.
======================================================================
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django (solo para superusuarios)
    # Accesible en: http://localhost:8000/admin/
    path("admin/", admin.site.urls),
    # URLs de autenticación integradas de Django
    # Incluye: login, logout, cambio de contraseña, etc.
    # Ruta base: /accounts/login/, /accounts/logout/, etc.
    path("accounts/", include("django.contrib.auth.urls")),
    # URLs de nuestra aplicación principal (app_principal/urls.py)
    # Al usar "" (vacío), las rutas de la app empiezan desde la raíz /
    # Ejemplo: /alumnos/, /materias/, /notas/, etc.
    path("", include("app_principal.urls")),
]
