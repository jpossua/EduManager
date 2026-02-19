"""
======================================================================
APPS.PY - Configuración de la aplicación "app_principal"
======================================================================
Cada app de Django necesita una clase de configuración que:
  1. Le dice a Django el nombre interno de la app (atributo 'name')
  2. Puede definir configuraciones adicionales (señales, verbose_name, etc.)

IMPORTANTE:
  - El atributo 'name' DEBE coincidir con el nombre de la carpeta de la app.
  - Si renombras la carpeta (ej: de 'core' a 'app_principal'),
    DEBES actualizar 'name' aquí Y en INSTALLED_APPS de settings.py.
  - 'default_auto_field' define el tipo de campo para las claves primarias
    automáticas (id). BigAutoField soporta hasta 9.2 quintillones de registros.
======================================================================
"""

from django.apps import AppConfig


class AppPrincipalConfig(AppConfig):
    # Tipo de campo automático para IDs: BigAutoField = entero grande (64 bits)
    default_auto_field = "django.db.models.BigAutoField"

    # Nombre de la app - DEBE coincidir con el nombre de la carpeta
    name = "app_principal"
