from django.db import models
from maestros.models import Region, Provincia, Comuna, Zona, Distrito, Grupo, EstadoCivil, Cargo, Nivel, Rama, Rol # Importar modelos maestros
from usuarios.models import Usuario # Importar Usuario

# Tabla: persona
class Persona(models.Model):
    # per_id: Identificador único de la persona (clave primaria)
    per_id = models.AutoField(primary_key=True)
    # esc_id: Clave foránea a EstadoCivil (relación ManyToOne)
    esc_id = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE, db_column='esc_id')
    # com_id: Clave foránea a Comuna (relación ManyToOne)
    com_id = models.ForeignKey(Comuna, on_delete=models.CASCADE, db_column='com_id')
    # usu_id: Clave foránea a Usuario (relación ManyToOne)
    usu_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='usu_id')
    # per_fecha_hora: Fecha y hora de registro/modificación
    per_fecha_hora = models.DateTimeField()
    # per_run: RUN de la persona (sin dígito verificador)
    per_run = models.IntegerField()
    # per_dv: Dígito verificador del RUN
    per_dv = models.CharField(max_length=1)
    # per_apelpat: Apellido paterno
    per_apelpat = models.CharField(max_length=50)
    # per_apelmat: Apellido materno
    per_apelmat = models.CharField(max_length=50, null=True, blank=True)
    # per_nombres: Nombres de la persona
    per_nombres = models.CharField(max_length=50)
    # per_email: Correo electrónico
    per_email = models.EmailField(max_length=100)
    # per_fecha_nac: Fecha de nacimiento
    per_fecha_nac = models.DateTimeField()
    # per_direccion: Dirección de la persona
    per_direccion = models.CharField(max_length=255)
    # per_tipo_fono: Tipo de teléfono (1: Fijo, 2: Celular, 3: Celular/WhatsApp, 4: WhatsApp)
    per_tipo_fono = models.IntegerField()
    # per_fono: Número de teléfono
    per_fono = models.CharField(max_length=15)
    # per_alergia_enfermedad: Alergias o enfermedades relevantes
    per_alergia_enfermedad = models.TextField(null=True, blank=True)
    # per_limitacion: Limitaciones físicas o de otro tipo
    per_limitacion = models.TextField(null=True, blank=True)
    # per_nom_emergencia: Nombre de contacto de emergencia
    per_nom_emergencia = models.CharField(max_length=50, null=True, blank=True)
    # per_fono_emergencia: Teléfono de contacto de emergencia
    per_fono_emergencia = models.CharField(max_length=15, null=True, blank=True)
    # per_otros: Otros datos relevantes
    per_otros = models.TextField(null=True, blank=True)
    # per_num_mmaa: Número de hijos/menores a cargo (si aplica)
    per_num_mmaa = models.IntegerField(null=True, blank=True)
    # per_profesion: Profesión u oficio
    per_profesion = models.CharField(max_length=100, null=True, blank=True)
    # per_tiempo_nnaj: Tiempo en situación de calle/vulnerabilidad (si aplica)
    per_tiempo_nnaj = models.CharField(max_length=50, null=True, blank=True)
    # per_tiempo_adulto: Tiempo como adulto responsable (si aplica)
    per_tiempo_adulto = models.CharField(max_length=50, null=True, blank=True)
    # per_religion: Religión
    per_religion = models.CharField(max_length=50, null=True, blank=True)
    # per_apodo: Apodo
    per_apodo = models.CharField(max_length=50)
    # per_foto: Ruta a la foto de la persona
    per_foto = models.TextField(null=True, blank=True)
    # per_vigente: Indica si la persona está activa (True) o inactiva (False)
    per_vigente = models.BooleanField()

    class Meta:
        db_table = 'persona'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f"{self.per_nombres} {self.per_apelpat}"

# Tabla: persona_grupo
class PersonaGrupo(models.Model):
    # peg_id: Identificador único de la relación (clave primaria)
    peg_id = models.AutoField(primary_key=True)
    # gru_id: Clave foránea a Grupo (relación ManyToOne)
    gru_id = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='gru_id')
    # per_id: Clave foránea a Persona (relación ManyToOne)
    per_id = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id')
    # peg_vigente: Indica si la relación está activa (True) o inactiva (False)
    peg_vigente = models.BooleanField()

    class Meta:
        db_table = 'persona_grupo'
        verbose_name = 'Persona en Grupo'
        verbose_name_plural = 'Personas en Grupos'
        unique_together = ('gru_id', 'per_id') # Asegura que una persona pertenezca a un grupo solo una vez

    def __str__(self):
        return f"{self.per_id} en {self.gru_id}"

# Tabla: persona_nivel
class PersonaNivel(models.Model):
    # pen_id: Identificador único de la relación (clave primaria)
    pen_id = models.AutoField(primary_key=True)
    # per_id: Clave foránea a Persona (relación ManyToOne)
    per_id = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id')
    # niv_id: Clave foránea a Nivel (relación ManyToOne)
    niv_id = models.ForeignKey(Nivel, on_delete=models.CASCADE, db_column='niv_id')
    # ram_id: Clave foránea a Rama (relación ManyToOne)
    ram_id = models.ForeignKey(Rama, on_delete=models.CASCADE, db_column='ram_id')

    class Meta:
        db_table = 'persona_nivel'
        verbose_name = 'Persona Nivel'
        verbose_name_plural = 'Personas Niveles'
        unique_together = ('per_id', 'niv_id', 'ram_id') # Asegura combinaciones únicas

    def __str__(self):
        return f"{self.per_id} - {self.niv_id} ({self.ram_id})"

# Tabla: persona_formador
class PersonaFormador(models.Model):
    # pef_id: Identificador único de la relación (clave primaria)
    pef_id = models.AutoField(primary_key=True)
    # per_id: Clave foránea a Persona (relación ManyToOne)
    per_id = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id')
    # pef_hab_1: Habilidad 1 (booleano)
    pef_hab_1 = models.BooleanField()
    # pef_hab_2: Habilidad 2 (booleano)
    pef_hab_2 = models.BooleanField()
    # pef_verif: Indicador de verificación (booleano)
    pef_verif = models.BooleanField()
    # pef_historial: Historial de capacitaciones de la persona
    pef_historial = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'persona_formador'
        verbose_name = 'Persona Formador'
        verbose_name_plural = 'Personas Formadores'

    def __str__(self):
        return f"Formador: {self.per_id}"

# Tabla: persona_individual
class PersonaIndividual(models.Model):
    # pei_id: Identificador único de la relación (clave primaria)
    pei_id = models.AutoField(primary_key=True)
    # per_id: Clave foránea a Persona (relación ManyToOne)
    per_id = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id')
    # car_id: Clave foránea a Cargo (relación ManyToOne)
    car_id = models.ForeignKey(Cargo, on_delete=models.CASCADE, db_column='car_id')
    # dis_id: Clave foránea a Distrito (relación ManyToOne, opcional)
    dis_id = models.ForeignKey(Distrito, on_delete=models.CASCADE, db_column='dis_id', null=True, blank=True)
    # zon_id: Clave foránea a Zona (relación ManyToOne, opcional)
    zon_id = models.ForeignKey(Zona, on_delete=models.CASCADE, db_column='zon_id', null=True, blank=True)
    # pei_vigente: Indica si la relación está activa (True) o inactiva (False)
    pei_vigente = models.BooleanField()

    class Meta:
        db_table = 'persona_individual'
        verbose_name = 'Persona Individual'
        verbose_name_plural = 'Personas Individuales'

    def __str__(self):
        return f"Individual: {self.per_id} - Cargo: {self.car_id}"

# Tabla: persona_vehiculo
class PersonaVehiculo(models.Model):
    # pev_id: Identificador único del vehículo (clave primaria)
    pev_id = models.AutoField(primary_key=True)
    # pec_id: Clave foránea a PersonaCurso (relación ManyToOne) - Nota: Esto parece ser un error en el esquema original, debería ser a Persona.
    # Asumiendo que debería ser a Persona, se corrige la clave foránea. Si es intencional, se debe revisar la lógica de negocio.
    # pev_id = models.ForeignKey('PersonaCurso', on_delete=models.CASCADE, db_column='pec_id') # Original
    per_id = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='per_id') # Corrección propuesta
    # pev_marca: Marca del vehículo
    pev_marca = models.CharField(max_length=50)
    # pev_modelo: Modelo del vehículo
    pev_modelo = models.CharField(max_length=50)
    # pev_patente: Patente del vehículo
    pev_patente = models.CharField(max_length=10)

    class Meta:
        db_table = 'persona_vehiculo'
        verbose_name = 'Vehículo de Persona'
        verbose_name_plural = 'Vehículos de Personas'

    def __str__(self):
        return f"{self.pev_marca} {self.pev_modelo} ({self.pev_patente})"
