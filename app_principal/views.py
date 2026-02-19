"""
======================================================================
VIEWS.PY - Vistas (Controladores de la aplicación)
======================================================================
Las vistas son el CORAZÓN de la lógica de la aplicación.
Cada vista es una función que:
  1. Recibe una petición HTTP (request)
  2. Procesa datos (consulta BD, valida formularios, etc.)
  3. Devuelve una respuesta HTTP (render de template, redirect, etc.)

Flujo típico de una vista:
  URL → Vista → Modelo (BD) → Template → HTML al navegador

Decoradores importantes:
  @login_required → Protege la vista: si el usuario no está autenticado,
                     lo redirige a LOGIN_URL (definido en settings.py).

Funciones clave de Django usadas aquí:
  - render():             Renderiza un template HTML con datos (contexto)
  - redirect():           Redirige a otra URL (usando el 'name' de urls.py)
  - get_object_or_404():  Busca un objeto en la BD o devuelve error 404
  - messages.success():   Muestra un mensaje flash verde al usuario
  - messages.error():     Muestra un mensaje flash rojo al usuario
======================================================================
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Materia, Alumno, Nota, Actividad
from django.contrib.auth.forms import UserCreationForm
from .forms import (
    RegistroProfesorForm,
    AlumnoForm,
    MateriaForm,
    ActividadForm,
    NotaForm,
)
from django.contrib import messages


# =====================================================================
# 1. DASHBOARD - Página principal del profesor
# =====================================================================
@login_required  # Solo usuarios autenticados pueden acceder
def dashboard(request):
    """
    Vista del panel principal. Muestra un resumen con:
    - Número de materias que tiene el profesor
    - Número total de alumnos (sin duplicados)

    request.user → Es el usuario actualmente logueado (profesor).
    Django lo inyecta automáticamente en cada petición gracias
    al middleware AuthenticationMiddleware.
    """
    # FILTRO DE SEGURIDAD: Solo traemos las materias de ESTE profesor
    # Cada profesor solo ve SU propia información
    materias = Materia.objects.filter(profesor=request.user)

    # Contamos alumnos únicos inscritos en las materias de este profesor
    # .distinct() evita contar un alumno 2 veces si está en 2 materias
    total_alumnos = Alumno.objects.filter(materias__in=materias).distinct().count()

    # 'contexto' es un diccionario con las variables disponibles en el template
    contexto = {
        "materias": materias,
        "total_alumnos": total_alumnos,
    }

    # render() combina el template HTML con los datos del contexto
    # y devuelve la página completa al navegador
    return render(request, "sistemas/dashboard.html", contexto)


# =====================================================================
# 2. CRUD DE ALUMNOS
# =====================================================================


@login_required
def lista_alumnos(request):
    """
    Muestra la lista de alumnos del profesor logueado.
    También prepara el formulario para el modal de crear alumno.
    """
    # Filtramos: Solo alumnos que cursan materias de ESTE profesor
    materias = Materia.objects.filter(profesor=request.user)
    alumnos = Alumno.objects.filter(materias__in=materias).distinct()

    # Creamos una instancia vacía del formulario para el modal de "Nuevo Alumno"
    # Pasamos user= para que el formulario solo muestre las materias del profesor
    form = AlumnoForm(user=request.user)

    contexto = {
        "materias": materias,
        "alumnos": alumnos,
        "form": form,
    }
    return render(request, "sistemas/lista_alumnos.html", contexto)


@login_required
def crear_alumno(request):
    """
    Crea un nuevo alumno. Solo acepta peticiones POST.
    Si el formulario es válido, guarda el alumno y redirige a la lista.
    Si no es válido, muestra un mensaje de error y redirige igualmente.
    """
    if request.method == "POST":
        # Pasamos request.POST (los datos del formulario) y user (para filtrar materias)
        form = AlumnoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()  # Guarda el alumno en la BD (incluyendo las materias M2M)
            messages.success(request, "Alumno creado correctamente.")
            return redirect("lista_alumnos")  # Redirige usando el 'name' de urls.py
        else:
            messages.error(
                request, "Error al crear el alumno. Por favor verifica los datos."
            )
    # Si no es POST o hay error, redirigimos a la lista
    return redirect("lista_alumnos")


@login_required
def editar_alumno(request, alumno_id):
    """
    Edita un alumno existente.
    - GET: Muestra el formulario con los datos actuales del alumno
    - POST: Guarda los cambios

    get_object_or_404(): Busca el alumno por ID.
    Si no existe, Django devuelve automáticamente una página 404.
    """
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if request.method == "POST":
        # instance=alumno: Le dice al formulario que estamos EDITANDO, no creando
        form = AlumnoForm(request.POST, instance=alumno, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumno actualizado correctamente.")
            return redirect("lista_alumnos")
    else:
        # En GET: Precargamos el formulario con los datos actuales del alumno
        form = AlumnoForm(instance=alumno, user=request.user)

    return render(
        request, "sistemas/editar_alumno.html", {"form": form, "alumno": alumno}
    )


@login_required
def eliminar_alumno(request, alumno_id):
    """
    Elimina un alumno. Solo acepta POST por seguridad.
    NUNCA se debe eliminar con GET porque los buscadores y bots
    podrían activar eliminaciones accidentales al rastrear enlaces.
    """
    alumno = get_object_or_404(Alumno, id=alumno_id)

    if request.method == "POST":
        alumno.delete()  # Elimina el registro de la BD
        messages.success(request, "Alumno eliminado correctamente.")

    return redirect("lista_alumnos")


# =====================================================================
# 3. CRUD DE MATERIAS
# =====================================================================


@login_required
def lista_materias(request):
    """Muestra las materias del profesor logueado con formulario modal."""
    materias = Materia.objects.filter(profesor=request.user)
    form = MateriaForm()
    return render(
        request, "sistemas/lista_materias.html", {"materias": materias, "form": form}
    )


@login_required
def crear_materia(request):
    """
    Crea una nueva materia.
    NOTA IMPORTANTE: Usamos form.save(commit=False) para obtener el objeto
    ANTES de guardarlo en la BD. Esto nos permite asignar el profesor
    manualmente (request.user) antes de hacer el save() definitivo.

    ¿Por qué? Porque el campo 'profesor' no está en el formulario
    (no queremos que el usuario lo vea ni lo modifique).
    """
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)  # Crea el objeto SIN guardarlo
            materia.profesor = request.user  # Asignamos el profesor logueado
            materia.save()  # Ahora sí guardamos en la BD
            messages.success(request, "Materia creada correctamente.")
            return redirect("lista_materias")
        else:
            messages.error(request, "Error al crear la materia.")
    return redirect("lista_materias")


@login_required
def editar_materia(request, materia_id):
    """
    Edita una materia existente.
    SEGURIDAD: Verificamos que la materia pertenezca al profesor logueado
    con profesor=request.user. Si otro profesor intenta editar una materia
    que no es suya, recibirá un error 404.
    """
    materia = get_object_or_404(Materia, id=materia_id, profesor=request.user)

    if request.method == "POST":
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            messages.success(request, "Materia actualizada correctamente.")
        else:
            messages.error(request, "Error al actualizar la materia.")

    return redirect("lista_materias")


@login_required
def eliminar_materia(request, materia_id):
    """Elimina una materia. Solo el profesor propietario puede hacerlo."""
    materia = get_object_or_404(Materia, id=materia_id, profesor=request.user)

    if request.method == "POST":
        materia.delete()
        messages.success(request, "Materia eliminada correctamente.")

    return redirect("lista_materias")


# =====================================================================
# 4. CRUD DE ACTIVIDADES
# =====================================================================


@login_required
def crear_actividad(request):
    """
    Crea una nueva actividad (examen, trabajo, práctica, etc.).
    El formulario ActividadForm filtra las materias para mostrar
    solo las del profesor logueado.
    """
    if request.method == "POST":
        form = ActividadForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Actividad creada correctamente.")
        else:
            messages.error(request, "Error al crear la actividad.")
    return redirect("registro_de_notas")


@login_required
def editar_actividad(request, actividad_id):
    """
    Edita una actividad existente.
    SEGURIDAD: Verificamos que la actividad pertenezca a una materia
    del profesor logueado usando materia__in=mis_materias.
    Esto previene que un profesor edite actividades de otro.
    """
    mis_materias = Materia.objects.filter(profesor=request.user)
    actividad = get_object_or_404(Actividad, id=actividad_id, materia__in=mis_materias)

    if request.method == "POST":
        form = ActividadForm(request.POST, instance=actividad, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Actividad actualizada correctamente.")
        else:
            messages.error(request, "Error al actualizar la actividad.")

    return redirect("registro_de_notas")


@login_required
def eliminar_actividad(request, actividad_id):
    """Elimina una actividad. Solo el profesor propietario puede hacerlo."""
    mis_materias = Materia.objects.filter(profesor=request.user)
    actividad = get_object_or_404(Actividad, id=actividad_id, materia__in=mis_materias)

    if request.method == "POST":
        actividad.delete()
        messages.success(request, "Actividad eliminada correctamente.")

    return redirect("registro_de_notas")


# =====================================================================
# 5. GESTIÓN DE CALIFICACIONES (NOTAS)
# =====================================================================


@login_required
def registro_de_notas(request):
    """
    Vista principal de calificaciones. La más compleja de todas porque:
    1. Procesa el formulario de creación de notas (POST)
    2. Muestra la lista de notas existentes
    3. Prepara formularios para modales (nota y actividad)
    4. Genera mapas JSON para filtros dinámicos en JavaScript

    Los mapas JSON se usan en el frontend para:
    - Filtrar alumnos según la materia seleccionada
    - Filtrar actividades según la materia seleccionada
    Sin recargar la página (experiencia más fluida).
    """
    mis_materias = Materia.objects.filter(profesor=request.user)

    # Procesar formulario de Nota (solo si es POST)
    if request.method == "POST":
        # -------------------------------------------------------------
        # VALIDACIÓN MANUAL PREVIA (Para mensajes personalizados)
        # -------------------------------------------------------------
        # Extraemos datos raw del POST para validar antes que el formulario
        alumno_id = request.POST.get("alumno")
        actividad_id = request.POST.get("actividad")
        nota_str = request.POST.get("nota")

        # 1. VALIDACIÓN DE RANGO DE NOTA
        try:
            # Intentamos convertir a float, si falla el form.is_valid lo atrapará
            if nota_str:
                nota_val = float(nota_str)
                if nota_val < 0 or nota_val > 10:
                    messages.error(request, "La nota debe estar entre 0 y 10.")
                    return redirect("registro_de_notas")
        except (ValueError, TypeError):
            pass

        # 2. VALIDACIÓN DE DUPLICADOS
        if alumno_id and actividad_id:
            if Nota.objects.filter(
                alumno_id=alumno_id, actividad_id=actividad_id
            ).exists():
                messages.error(
                    request,
                    "No se puede calificar al alumno de la misma actividad dos veces.",
                )
                return redirect("registro_de_notas")

            # 3. VALIDACIÓN DE INSCRIPCIÓN
            try:
                alumno_obj = Alumno.objects.get(id=alumno_id)
                actividad_obj = Actividad.objects.get(id=actividad_id)
                if actividad_obj.materia not in alumno_obj.materias.all():
                    messages.error(
                        request,
                        f"Error: El alumno {alumno_obj.nombre} no está inscrito en la materia '{actividad_obj.materia.nombre}'.",
                    )
                    return redirect("registro_de_notas")
            except (Alumno.DoesNotExist, Actividad.DoesNotExist):
                pass

        # Si pasa las validaciones manuales, procesamos el formulario normalmente
        form = NotaForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Calificación registrada correctamente.")
            except Exception as e:
                messages.error(request, f"Error inesperado: {str(e)}")
            return redirect("registro_de_notas")
        else:
            # Si hay otros errores (ej: campos vacíos, formato incorrecto)
            for field, errors in form.errors.items():
                for error in errors:
                    # Filtramos errores de duplicados si se colaron (aunque la validación manual debería haberlos atrapado)
                    if "already exists" not in str(error) and "ya existe" not in str(
                        error
                    ):
                        messages.error(request, error)

    # Obtenemos TODAS las notas de los alumnos en mis materias
    # order_by('-id'): Las más recientes primero (ID más alto = más nuevo)
    notas = Nota.objects.filter(actividad__materia__in=mis_materias).order_by("-id")

    # Listas de alumnos y actividades para los desplegables del formulario
    alumnos = Alumno.objects.filter(materias__in=mis_materias).distinct()
    actividades = Actividad.objects.filter(materia__in=mis_materias).order_by("-fecha")

    # Formularios vacíos para los modales
    form_nota = NotaForm(user=request.user)
    form_actividad = ActividadForm(user=request.user)

    # -----------------------------------------------------------------
    # MAPAS JSON para filtros dinámicos en JavaScript
    # -----------------------------------------------------------------
    # actividad_materia_map: {id_actividad: id_materia}
    # Ejemplo: {"1": "5", "2": "5", "3": "8"}
    # → La actividad 1 pertenece a la materia 5
    actividad_materia_map = {str(act.id): str(act.materia.id) for act in actividades}

    # alumno_materias_map: {id_alumno: [lista de ids de materias]}
    # Ejemplo: {"7": [5, 8], "10": [5]}
    # → El alumno 7 está en las materias 5 y 8
    alumno_materias_map = {
        str(al.id): list(al.materias.values_list("id", flat=True)) for al in alumnos
    }

    return render(
        request,
        "sistemas/notas.html",
        {
            "notas": notas,
            "alumnos": alumnos,
            "actividades": actividades,
            "form_nota": form_nota,
            "form_actividad": form_actividad,
            "actividad_materia_map": actividad_materia_map,
            "alumno_materias_map": alumno_materias_map,
        },
    )


@login_required
def editar_nota(request, nota_id):
    """
    Edita la calificación de una nota existente.
    Recibe el nuevo valor por POST y valida que esté entre 0 y 10.

    SEGURIDAD: Usamos actividad__materia__in=mis_materias para
    asegurarnos de que la nota pertenezca a una actividad de una
    materia del profesor logueado.
    """
    mis_materias = Materia.objects.filter(profesor=request.user)
    nota_obj = get_object_or_404(Nota, id=nota_id, actividad__materia__in=mis_materias)

    if request.method == "POST":
        try:
            # Convertimos el valor recibido a float
            nueva_nota = float(request.POST.get("nota", ""))
            if 0 <= nueva_nota <= 10:
                nota_obj.nota = nueva_nota
                nota_obj.full_clean()  # Ejecuta TODAS las validaciones del modelo
                nota_obj.save()
                messages.success(request, "Nota actualizada correctamente.")
            else:
                messages.error(request, "La nota debe estar entre 0 y 10.")
        except (ValueError, TypeError):
            # ValueError: Si el usuario envía texto en vez de número
            # TypeError: Si el valor es None
            messages.error(request, "Valor de nota inválido.")

    return redirect("registro_de_notas")


@login_required
def eliminar_nota(request, nota_id):
    """Elimina una nota. Solo el profesor propietario puede hacerlo."""
    mis_materias = Materia.objects.filter(profesor=request.user)
    nota = get_object_or_404(Nota, id=nota_id, actividad__materia__in=mis_materias)

    if request.method == "POST":
        nota.delete()
        messages.success(request, "Nota eliminada correctamente.")

    return redirect("registro_de_notas")


# =====================================================================
# 6. REGISTRO DE PROFESOR (Página pública)
# =====================================================================
# Esta vista NO tiene @login_required porque es pública:
# cualquier persona puede registrarse como profesor.
def registro_profesor(request):
    """
    Permite a un nuevo profesor crear su cuenta.
    - GET: Muestra el formulario de registro vacío
    - POST: Valida y crea la cuenta, luego redirige al login
    """
    if request.method == "POST":
        form = RegistroProfesorForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el usuario en la BD
            messages.success(request, "Cuenta creada. Por favor inicia sesión.")
            return redirect("login")
    else:
        # En GET: Mostramos el formulario vacío
        form = RegistroProfesorForm()

    return render(request, "registros/registro.html", {"form": form})
