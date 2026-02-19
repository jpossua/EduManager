"""
======================================================================
FORMS.PY - Formularios de Django
======================================================================
Los formularios en Django manejan:
  1. Generar el HTML de los inputs automáticamente
  2. Validar los datos enviados por el usuario
  3. Guardar los datos en la base de datos

Tipos principales:
  - forms.Form: Formulario libre (sin modelo asociado)
  - forms.ModelForm: Formulario que SE CONECTA a un modelo de la BD
    → Genera los campos automáticamente desde el modelo
    → El método save() guarda directamente en la BD

Widgets: Controlan CÓMO se renderiza cada campo en HTML.
  - forms.TextInput   → <input type="text">
  - forms.EmailInput  → <input type="email">
  - forms.Select      → <select>...</select>
  - forms.DateInput   → <input type="date">
  - forms.NumberInput  → <input type="number">
======================================================================
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm  # Formulario base de registro
from django.contrib.auth.models import User
from .models import Alumno, Materia, Actividad, Nota


# =====================================================================
# 1. FORMULARIO: REGISTRO DE PROFESOR
# =====================================================================
# Hereda de UserCreationForm que ya incluye:
#   - Campo 'username' (nombre de usuario)
#   - Campo 'password1' (contraseña)
#   - Campo 'password2' (confirmar contraseña)
# Nosotros le agregamos: email, first_name, last_name
class RegistroProfesorForm(UserCreationForm):
    class Meta:
        model = User  # Se conecta al modelo User de Django
        # Campos que se mostrarán en el formulario
        # UserCreationForm.Meta.fields ya incluye 'username'
        # Le sumamos email, nombre y apellido con el operador +
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        __init__: Se ejecuta al crear una instancia del formulario.
        Aquí recorremos TODOS los campos y les añadimos la clase CSS
        'form-control' de Bootstrap para que se vean estilizados.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # Solo agregamos la clase si el campo no tiene una ya definida
            if "class" not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs["class"] = "form-control"
            # Mantenemos las etiquetas originales del campo
            self.fields[field].label = self.fields[field].label


# =====================================================================
# 2. FORMULARIO: ALUMNO (ModelForm)
# =====================================================================
# Se conecta al modelo Alumno y genera campos para: nombre, correo, materias
class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ["nombre", "correo", "materias"]
        # widgets: Personalizamos cómo se renderiza cada campo en HTML
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre completo"}
            ),
            "correo": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Correo electrónico"}
            ),
            # CheckboxSelectMultiple: Muestra las materias como checkboxes
            # en lugar de un <select multiple>. Más intuitivo para el usuario.
            "materias": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        """
        Recibimos el usuario logueado a través de kwargs.
        kwargs.pop('user') extrae y elimina 'user' del diccionario,
        porque Django no espera ese parámetro en el constructor del form.
        """
        user = kwargs.pop("user", None)  # Extraemos el usuario del profesor
        super().__init__(*args, **kwargs)

        # Mensaje de error personalizado para el campo 'materias'
        self.fields["materias"].error_messages[
            "required"
        ] = "¡Error, este campo es obligatorio!"

        if user:
            # FILTRO DE SEGURIDAD: Solo mostramos las materias del profesor logueado
            # Sin este filtro, un profesor vería las materias de TODOS los profesores
            self.fields["materias"].queryset = Materia.objects.filter(profesor=user)

        # Aseguramos que los campos tengan la clase Bootstrap
        for field in ["nombre", "correo"]:
            if "class" not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs["class"] = "form-control"


# =====================================================================
# 3. FORMULARIO: MATERIA (ModelForm)
# =====================================================================
# Formulario simple con solo el campo 'nombre'.
# El campo 'profesor' se asigna automáticamente en la vista (views.py)
# usando form.save(commit=False) para no guardar el registro incompleto.
class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ["nombre"]  # Solo el nombre; el profesor se asigna en la vista
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la materia"}
            ),
        }


# =====================================================================
# 4. FORMULARIO: ACTIVIDAD (ModelForm)
# =====================================================================
# Permite crear exámenes, trabajos, prácticas, etc.
# Los campos materia y categoría usan <select> (desplegables).
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["materia", "nombre", "categoria", "fecha"]
        widgets = {
            # form-select: Clase Bootstrap para <select> estilizados
            "materia": forms.Select(attrs={"class": "form-select"}),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Examen Parcial 1"}
            ),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            # type='date': Muestra un selector de fecha nativo del navegador
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            # Solo mostramos las materias del profesor logueado en el desplegable
            self.fields["materia"].queryset = Materia.objects.filter(profesor=user)


# =====================================================================
# 5. FORMULARIO: NOTA (ModelForm)
# =====================================================================
# El formulario más complejo: tiene validación personalizada en clean().
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ["alumno", "actividad", "nota"]
        widgets = {
            "alumno": forms.Select(attrs={"class": "form-select"}),
            "actividad": forms.Select(attrs={"class": "form-select"}),
            "nota": forms.NumberInput(
                # step=0.1: Permite decimales como 8.5
                # Eliminamos min/max para validar solo en el backend (views.py)
                attrs={"class": "form-control", "step": 0.1}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtramos SOLO las materias de este profesor
            mis_materias = Materia.objects.filter(profesor=user)

            # Solo mostramos alumnos inscritos en las materias de este profesor
            # .distinct(): Evita duplicados si un alumno está en varias materias
            self.fields["alumno"].queryset = Alumno.objects.filter(
                materias__in=mis_materias
            ).distinct()

            # Solo mostramos actividades de las materias de este profesor
            self.fields["actividad"].queryset = Actividad.objects.filter(
                materia__in=mis_materias
            )

    def clean(self):
        """
        Validación personalizada a nivel de formulario.
        Se ejecuta DESPUÉS de que cada campo individual se haya validado.

        Aquí verificamos una REGLA DE NEGOCIO importante:
        El alumno debe estar inscrito en la materia de la actividad.
        Ejemplo: Si la actividad es "Examen de Matemáticas", el alumno
        debe estar inscrito en "Matemáticas".
        """
        cleaned_data = super().clean()  # Datos ya validados individualmente
        alumno = cleaned_data.get("alumno")
        actividad = cleaned_data.get("actividad")

        if alumno and actividad:
            # Verificamos si el alumno está inscrito en la materia de la actividad
            if not alumno.materias.filter(id=actividad.materia.id).exists():
                raise forms.ValidationError(
                    f"{alumno.nombre} no está inscrito en {actividad.materia.nombre}."
                )

        return cleaned_data
