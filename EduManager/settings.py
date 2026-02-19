"""
======================================================================
SETTINGS.PY - Configuración central del proyecto Django
======================================================================
Este es el archivo MÁS IMPORTANTE del proyecto. Aquí se configura TODO:
  - Qué apps están instaladas (INSTALLED_APPS)
  - Cómo conectar a la base de datos (DATABASES)
  - Dónde buscar las plantillas HTML (TEMPLATES)
  - Configuración de seguridad, idioma, zona horaria, etc.

REGLA DE ORO: Si algo no funciona, probablemente hay que revisar aquí.
======================================================================
"""

from pathlib import Path

# =====================================================================
# RUTA BASE DEL PROYECTO
# =====================================================================
# BASE_DIR apunta a la carpeta raíz del proyecto (donde está manage.py)
# Se usa para construir rutas absolutas como: BASE_DIR / 'db.sqlite3'
# Path(__file__) → ruta de este archivo (settings.py)
# .resolve()    → convierte a ruta absoluta
# .parent       → sube un nivel (a EduManager/)
# .parent       → sube otro nivel (a gestion_escolar/)
BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================================
# SEGURIDAD
# =====================================================================

# SECRET_KEY: Clave criptográfica que Django usa para firmar cookies,
# tokens CSRF y sesiones. En PRODUCCIÓN debe ser secreta y única.
# NUNCA la compartas ni la subas a GitHub.
SECRET_KEY = "django-insecure-t%h7%+ma!1qjob3dcqp2a4fd+@4sumapp_o*%f#a)#be##197b"

# DEBUG = True: Muestra errores detallados en el navegador.
# En PRODUCCIÓN esto DEBE ser False por seguridad.
DEBUG = True

# ALLOWED_HOSTS: Lista de dominios/IPs que pueden acceder al sitio.
# En desarrollo incluimos localhost y el dominio local de Laragon.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "gestion-escolar.test"]


# =====================================================================
# APLICACIONES INSTALADAS
# =====================================================================
# Django viene con apps internas (admin, auth, sessions...).
# Nuestra app personalizada 'app_principal' se agrega al final.
# IMPORTANTE: Si creas una app nueva con 'python manage.py startapp',
# DEBES registrarla aquí para que Django la reconozca.
INSTALLED_APPS = [
    "django.contrib.admin",  # Panel de administración
    "django.contrib.auth",  # Sistema de autenticación (login, permisos)
    "django.contrib.contenttypes",  # Framework de tipos de contenido
    "django.contrib.sessions",  # Manejo de sesiones de usuario
    "django.contrib.messages",  # Sistema de mensajes flash (éxito, error)
    "django.contrib.staticfiles",  # Manejo de archivos estáticos (CSS, JS, imágenes)
    "app_principal",  # ← Nuestra app de gestión escolar
]


# =====================================================================
# MIDDLEWARE (Capas intermedias de procesamiento)
# =====================================================================
# Los middleware son "filtros" que procesan cada petición HTTP
# ANTES de llegar a tu vista y DESPUÉS de que tu vista responde.
# El orden importa: se ejecutan de arriba a abajo en la petición
# y de abajo a arriba en la respuesta.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Seguridad HTTPS, headers, etc.
    "django.contrib.sessions.middleware.SessionMiddleware",  # Habilita las sesiones
    "django.middleware.common.CommonMiddleware",  # Normaliza URLs (trailing slash)
    "django.middleware.csrf.CsrfViewMiddleware",  # Protección contra ataques CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Asocia usuario a cada petición
    "django.contrib.messages.middleware.MessageMiddleware",  # Habilita mensajes flash
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Protección contra clickjacking
]


# =====================================================================
# CONFIGURACIÓN DE URLs
# =====================================================================
# ROOT_URLCONF: Indica qué archivo contiene las URLs principales.
# Django busca la variable 'urlpatterns' en este módulo.
ROOT_URLCONF = "EduManager.urls"


# =====================================================================
# CONFIGURACIÓN DE PLANTILLAS (TEMPLATES)
# =====================================================================
# Django busca las plantillas HTML en las carpetas 'templates/'
# dentro de cada app cuando APP_DIRS = True.
# Ruta resultante: app_principal/templates/sistemas/dashboard.html
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Aquí puedes agregar carpetas de templates globales
        "APP_DIRS": True,  # True = busca templates dentro de cada app
        "OPTIONS": {
            # context_processors inyectan variables globales a TODOS los templates
            "context_processors": [
                "django.template.context_processors.request",  # Variable 'request'
                "django.contrib.auth.context_processors.auth",  # Variable 'user'
                "django.contrib.messages.context_processors.messages",  # Variable 'messages'
            ],
        },
    },
]

# WSGI_APPLICATION: Punto de entrada para el servidor de producción
WSGI_APPLICATION = "EduManager.wsgi.application"


# =====================================================================
# BASE DE DATOS
# =====================================================================
# Tenemos dos configuraciones:
# 1. 'default' → SQLite: Base de datos ligera en un archivo local.
#    Perfecta para desarrollo. No requiere instalación.
# 2. 'mysql_db' → MySQL: Para producción o si necesitas más potencia.
#    Requiere tener MySQL/MariaDB instalado (Laragon lo incluye).
#
# Para usar MySQL en vez de SQLite, cambia 'default' por la config de MySQL.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Motor de BD
        "NAME": BASE_DIR / "db.sqlite3",  # Ruta del archivo SQLite
    },
    "mysql_db": {
        "ENGINE": "django.db.backends.mysql",  # Motor MySQL
        "NAME": "gestion_escolar",  # Nombre de la BD en MySQL
        "USER": "root",  # Usuario (root en desarrollo)
        "PASSWORD": "",  # Contraseña (vacía en Laragon)
        "HOST": "localhost",  # Servidor
        "PORT": "3306",  # Puerto por defecto de MySQL
    },
}


# =====================================================================
# VALIDADORES DE CONTRASEÑA
# =====================================================================
# Django valida las contraseñas de los usuarios con estas reglas:
AUTH_PASSWORD_VALIDATORS = [
    {
        # No permite contraseñas similares al nombre de usuario o email
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        # Contraseña mínima de 8 caracteres por defecto
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        # Rechaza contraseñas muy comunes ('123456', 'password', etc.)
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        # Rechaza contraseñas que sean solo números
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =====================================================================
# INTERNACIONALIZACIÓN (Idioma y Zona Horaria)
# =====================================================================
LANGUAGE_CODE = "es-ES"  # Idioma: Español de España
TIME_ZONE = "Europe/Madrid"  # Zona horaria: España peninsular
USE_I18N = True  # Activar sistema de traducción
USE_TZ = True  # Usar zona horaria en las fechas


# =====================================================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# =====================================================================
# STATIC_URL: Prefijo de URL para acceder a archivos estáticos.
# Ejemplo: /static/app_principal/img/logo.png
STATIC_URL = "static/"


# =====================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN (Login/Logout)
# =====================================================================
# LOGIN_REDIRECT_URL: ¿A dónde va el usuario DESPUÉS de hacer login?
# '/' redirige al dashboard (la página principal)
LOGIN_REDIRECT_URL = "/"

# LOGOUT_REDIRECT_URL: ¿A dónde va el usuario DESPUÉS de cerrar sesión?
LOGOUT_REDIRECT_URL = "/login/"

# LOGIN_URL: ¿A dónde redirigir si el usuario NO está autenticado?
# Usado por el decorador @login_required
LOGIN_URL = "/login/"
