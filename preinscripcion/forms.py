from django import forms
from django.core.exceptions import ValidationError
from backend.personas.models import Persona
from backend.usuarios.models import Usuario
from backend.maestros.models import EstadoCivil, Comuna, Provincia, Region # Assuming these are the correct paths

class PersonaForm(forms.ModelForm):
    # Campos para RUN y DV
    per_run = forms.IntegerField(label="RUN (sin dígito verificador)", required=True)
    per_dv = forms.CharField(label="Dígito Verificador", max_length=1, required=True)

    # Campos de texto y email
    per_nombres = forms.CharField(label="Nombres", max_length=50, required=True)
    per_apelpat = forms.CharField(label="Apellido Paterno", max_length=50, required=True)
    per_apelmat = forms.CharField(label="Apellido Materno", max_length=50, required=False)
    per_apodo = forms.CharField(label="Apodo", max_length=50, required=True)
    per_email = forms.EmailField(label="Correo Electrónico", max_length=100, required=True)
    per_fecha_nac = forms.DateField(label="Fecha de Nacimiento", widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    per_direccion = forms.CharField(label="Dirección", max_length=255, required=True)

    # Campos de selección (ForeignKey)
    # Nota: Para Comuna, Provincia, Region, se necesitará lógica adicional en el view/frontend para carga dinámica.
    # Aquí se definen como ModelChoiceField, Django intentará mostrar todas las opciones.
    esc_id = forms.ModelChoiceField(queryset=EstadoCivil.objects.filter(esc_vigente=True), label="Estado Civil", required=True)
    reg_id = forms.ModelChoiceField(queryset=Region.objects.filter(reg_vigente=True), label="Región", required=True)
    pro_id = forms.ModelChoiceField(queryset=Provincia.objects.filter(pro_vigente=True), label="Provincia", required=True)
    com_id = forms.ModelChoiceField(queryset=Comuna.objects.filter(com_vigente=True), label="Comuna", required=True)

    # Campos de teléfono
    per_tipo_fono = forms.ChoiceField(
        label="Tipo de Teléfono",
        choices=[(1, 'Fijo'), (2, 'Celular'), (3, 'Celular/WhatsApp'), (4, 'WhatsApp')],
        widget=forms.RadioSelect,
        required=True
    )
    per_fono = forms.CharField(label="Número de Teléfono", max_length=15, required=True)

    # Campos opcionales de texto
    per_alergia_enfermedad = forms.CharField(label="Alergias o Enfermedades", widget=forms.Textarea, required=False)
    per_limitacion = forms.CharField(label="Limitaciones", widget=forms.Textarea, required=False)
    per_nom_emergencia = forms.CharField(label="Nombre Contacto de Emergencia", max_length=50, required=False)
    per_fono_emergencia = forms.CharField(label="Teléfono Contacto de Emergencia", max_length=15, required=False)
    per_otros = forms.CharField(label="Otros Datos Relevantes", widget=forms.Textarea, required=False)
    per_num_mmaa = forms.IntegerField(label="Número de Hijos/Menores a Cargo", required=False, min_value=0)
    per_profesion = forms.CharField(label="Profesión u Oficio", max_length=100, required=False)
    per_tiempo_nnaj = forms.CharField(label="Tiempo en situación de calle/vulnerabilidad", max_length=50, required=False)
    per_tiempo_adulto = forms.CharField(label="Tiempo como adulto responsable", max_length=50, required=False)
    per_religion = forms.CharField(label="Religión", max_length=50, required=False)

    # Campo de carga de archivo
    per_foto = forms.ImageField(label="Foto de Perfil", required=False)

    class Meta:
        model = Persona
        fields = [
            'per_run', 'per_dv', 'per_nombres', 'per_apelpat', 'per_apelmat', 'per_apodo',
            'per_email', 'per_fecha_nac', 'per_direccion', 'reg_id', 'pro_id', 'com_id', 'esc_id',
            'per_tipo_fono', 'per_fono', 'per_alergia_enfermedad', 'per_limitacion',
            'per_nom_emergencia', 'per_fono_emergencia', 'per_otros', 'per_num_mmaa',
            'per_profesion', 'per_tiempo_nnaj', 'per_tiempo_adulto', 'per_religion',
            'per_foto'
        ]

    def clean_per_dv(self):
        per_run = self.cleaned_data.get('per_run')
        per_dv = self.cleaned_data.get('per_dv')

        if per_run is not None and per_dv:
            # Lógica para validar RUN y DV
            dv_calculado = self.calcular_dv(per_run)
            if dv_calculado.upper() != per_dv.upper():
                raise ValidationError("El dígito verificador no es válido para el RUN ingresado.")
        return per_dv

    def calcular_dv(self, run):
        # Implementación simplificada del cálculo del dígito verificador
        if not run:
            return ''
        run_str = str(run)
        f = 2
        s = 0
        while run_str:
            s += int(run_str[-1]) * f
            run_str = run_str[:-1]
            f = 3 if f > 6 else f + 1
        dv = 11 - (s % 11)
        if dv == 11:
            return '0'
        elif dv == 10:
            return 'K'
        else:
            return str(dv)

    # Override __init__ to handle dynamic filtering of FKs
    def __init__(self, *args, **kwargs):
        # Extract reg_id and pro_id from kwargs if they are passed
        self.reg_id = kwargs.pop('reg_id', None)
        self.pro_id = kwargs.pop('pro_id', None)

        super().__init__(*args, **kwargs)

        # Explicitly declare types to help Pylance resolve attribute access
        # This ensures Pylance recognizes the 'queryset' attribute.
        pro_field: forms.ModelChoiceField = self.fields['pro_id']
        com_field: forms.ModelChoiceField = self.fields['com_id']

        # Filter Provincia queryset based on reg_id
        if self.reg_id:
            pro_field.queryset = Provincia.objects.filter(reg_id=self.reg_id, pro_vigente=True)
        else:
            pro_field.queryset = Provincia.objects.none()

        # Filter Comuna queryset based on pro_id
        if self.pro_id:
            com_field.queryset = Comuna.objects.filter(pro_id=self.pro_id, com_vigente=True)
        else:
            com_field.queryset = Comuna.objects.none()

        # Ensure required fields are marked as required in the form definition
        self.fields['per_run'].required = True
        self.fields['per_dv'].required = True
        self.fields['per_nombres'].required = True
        self.fields['per_apelpat'].required = True
        self.fields['per_apodo'].required = True
        self.fields['per_email'].required = True
        self.fields['per_fecha_nac'].required = True
        self.fields['per_direccion'].required = True
        self.fields['esc_id'].required = True
        self.fields['reg_id'].required = True
        self.fields['pro_id'].required = True
        self.fields['com_id'].required = True
        self.fields['per_tipo_fono'].required = True
        self.fields['per_fono'].required = True


class UsuarioForm(forms.ModelForm):
    usu_username = forms.CharField(label="Nombre de Usuario", max_length=100, required=True)
    usu_password = forms.CharField(label="Contraseña", max_length=128, widget=forms.PasswordInput, required=True)
    usu_password_confirm = forms.CharField(label="Confirmar Contraseña", max_length=128, widget=forms.PasswordInput, required=True)

    class Meta:
        model = Usuario
        fields = ['usu_username', 'usu_password'] # Excluimos usu_id, pel_id, usu_ruta_foto, usu_vigente

    def clean_usu_password_confirm(self):
        password = self.cleaned_data.get("usu_password")
        password_confirm = self.cleaned_data.get("usu_password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return password_confirm

    def save(self, commit=True):
        # Sobrescribir save para hashear la contraseña antes de guardarla
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["usu_password"])
        if commit:
            user.save()
        return user

# Nota: Para la preinscripción, es común que el backend cree un objeto Persona y Usuario.
# La lógica para asociar Persona con Usuario (usu_id en Persona) y para asignar un perfil por defecto
# a Usuario (pel_id) se manejaría en la vista que utiliza estos formularios.
# Por ejemplo, en la vista de preinscripción:
# if request.method == 'POST':
#     persona_form = PersonaForm(request.POST, request.FILES)
#     usuario_form = UsuarioForm(request.POST)
#     if persona_form.is_valid() and usuario_form.is_valid():
#         usuario = usuario_form.save() # Guarda el usuario hasheando la contraseña
#         persona = persona_form.save(commit=False)
#         persona.usu_id = usuario # Asocia el usuario creado
#         # Asignar valores por defecto para campos no incluidos en el formulario
#         persona.per_vigente = True # O False si requiere validación
#         persona.per_fecha_hora = timezone.now()
#         # Asignar un perfil por defecto al usuario si es necesario
#         # default_profile = Perfil.objects.get(pel_descripcion='Preinscrito') # Ejemplo
#         # usuario.pel_id = default_profile
#         # usuario.save()
#         persona.save()
#         # Redirigir o mostrar mensaje de éxito
