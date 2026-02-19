"""
======================================================================
URLS.PY (App) - Rutas de la aplicación principal
======================================================================
Aquí definimos TODAS las URLs de nuestra app y las conectamos
con sus vistas correspondientes.

Cada path() tiene 3 partes:
  1. La URL (ej: "alumnos/")
  2. La vista que se ejecuta (ej: views.lista_alumnos)
  3. El 'name' para referenciar la URL en templates (ej: name="lista_alumnos")

El 'name' es CRUCIAL porque permite usar {% url 'nombre' %} en los
templates en lugar de escribir URLs hardcodeadas. Si cambias la URL,
los templates se actualizan automáticamente.

Parámetros dinámicos:
  <int:alumno_id> → Captura un número entero de la URL y lo pasa
                     como argumento a la vista.
  Ejemplo: /alumnos/editar/5/ → alumno_id=5
======================================================================
"""

from django.urls import path
from . import views  # Importamos las vistas de nuestra app
from django.contrib.auth import views as auth_views  # Vistas de autenticación de Django

urlpatterns = [
    # =================================================================
    # DASHBOARD - Página principal (requiere login)
    # =================================================================
    path("", views.dashboard, name="dashboard"),
    # =================================================================
    # CRUD DE ALUMNOS
    # =================================================================
    # Listar todos los alumnos del profesor logueado
    path("alumnos/", views.lista_alumnos, name="lista_alumnos"),
    # Crear un nuevo alumno (solo acepta POST desde el modal)
    path("alumnos/crear/", views.crear_alumno, name="crear_alumno"),
    # Editar un alumno existente - <int:alumno_id> captura el ID del alumno
    path("alumnos/editar/<int:alumno_id>/", views.editar_alumno, name="editar_alumno"),
    # Eliminar un alumno (solo acepta POST por seguridad)
    path(
        "alumnos/eliminar/<int:alumno_id>/",
        views.eliminar_alumno,
        name="eliminar_alumno",
    ),
    # =================================================================
    # CRUD DE MATERIAS
    # =================================================================
    path("materias/", views.lista_materias, name="lista_materias"),
    path("materias/crear/", views.crear_materia, name="crear_materia"),
    path(
        "materias/editar/<int:materia_id>/", views.editar_materia, name="editar_materia"
    ),
    path(
        "materias/eliminar/<int:materia_id>/",
        views.eliminar_materia,
        name="eliminar_materia",
    ),
    # =================================================================
    # CALIFICACIONES Y ACTIVIDADES
    # =================================================================
    # Página principal de notas (listar, crear notas)
    path("notas/", views.registro_de_notas, name="registro_de_notas"),
    # Editar y eliminar notas individuales
    path("notas/editar/<int:nota_id>/", views.editar_nota, name="editar_nota"),
    path("notas/eliminar/<int:nota_id>/", views.eliminar_nota, name="eliminar_nota"),
    # CRUD de actividades (exámenes, trabajos, prácticas)
    path("actividades/crear/", views.crear_actividad, name="crear_actividad"),
    path(
        "actividades/editar/<int:actividad_id>/",
        views.editar_actividad,
        name="editar_actividad",
    ),
    path(
        "actividades/eliminar/<int:actividad_id>/",
        views.eliminar_actividad,
        name="eliminar_actividad",
    ),
    # =================================================================
    # AUTENTICACIÓN (Login, Logout, Registro)
    # =================================================================
    # Registro público: Cualquier profesor puede crear su cuenta
    path("registro/", views.registro_profesor, name="registro_profesor"),
    # Login: Usamos la vista genérica de Django LoginView
    # pero con nuestro template personalizado en registros/login.html
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registros/login.html"),
        name="login",
    ),
    # Logout: Django se encarga de cerrar la sesión
    # Redirige a LOGOUT_REDIRECT_URL definido en settings.py
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
