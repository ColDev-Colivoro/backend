from django.utils import timezone
from unittest.mock import MagicMock

# Mocking foreign key dependencies
mock_estado_civil = MagicMock()
mock_estado_civil.pk = 1
mock_estado_civil.esc_descripcion = "Soltero"

mock_comuna = MagicMock()
mock_comuna.pk = 1
mock_comuna.com_descripcion = "Santiago Centro"

mock_usuario = MagicMock()
mock_usuario.pk = 1
mock_usuario.usu_username = "mockuser"

mock_grupo = MagicMock()
mock_grupo.pk = 1
mock_grupo.gru_descripcion = "Grupo A"
mock_nivel = MagicMock()
mock_nivel.pk = 1
mock_nivel.niv_descripcion = "Nivel 1"
mock_rama = MagicMock()
mock_rama.pk = 1
mock_rama.ram_descripcion = "Rama X"
mock_cargo = MagicMock()
mock_cargo.pk = 1
mock_cargo.car_descripcion = "Cargo Y"
mock_distrito = MagicMock()
mock_zona = MagicMock()


# --- Mocking the Models from the 'personas' app ---

class Persona:
    def __init__(self, per_id=1, esc_id=None, com_id=None, usu_id=None, per_fecha_hora=None, per_run=12345678, per_dv="9", per_apelpat="Perez", per_apelmat="Gonzalez", per_nombres="Juan", per_email="juan.perez@example.com", per_fecha_nac=None, per_direccion="Calle Falsa 123", per_tipo_fono=2, per_fono="987654321", per_alergia_enfermedad=None, per_limitacion=None, per_nom_emergencia="Maria", per_fono_emergencia="11223344", per_otros=None, per_num_mmaa=2, per_profesion="Ingeniero", per_tiempo_nnaj="1 año", per_tiempo_adulto="5 años", per_religion="Católica", per_apodo="Juanito", per_foto=None, per_vigente=True):
        self.per_id = per_id
        self.esc_id = esc_id
        self.com_id = com_id
        self.usu_id = usu_id
        self.per_fecha_hora = per_fecha_hora if per_fecha_hora else timezone.now()
        self.per_run = per_run
        self.per_dv = per_dv
        self.per_apelpat = per_apelpat
        self.per_apelmat = per_apelmat
        self.per_nombres = per_nombres
        self.per_email = per_email
        self.per_fecha_nac = per_fecha_nac if per_fecha_nac else timezone.datetime(1990, 5, 15)
        self.per_direccion = per_direccion
        self.per_tipo_fono = per_tipo_fono
        self.per_fono = per_fono
        self.per_alergia_enfermedad = per_alergia_enfermedad
        self.per_limitacion = per_limitacion
        self.per_nom_emergencia = per_nom_emergencia
        self.per_fono_emergencia = per_fono_emergencia
        self.per_otros = per_otros
        self.per_num_mmaa = per_num_mmaa
        self.per_profesion = per_profesion
        self.per_tiempo_nnaj = per_tiempo_nnaj
        self.per_tiempo_adulto = per_tiempo_adulto
        self.per_religion = per_religion
        self.per_apodo = per_apodo
        self.per_foto = per_foto
        self.per_vigente = per_vigente

    def __str__(self):
        return f"{self.per_nombres} {self.per_apelpat}"

class PersonaGrupo:
    def __init__(self, peg_id=1, gru_id=None, per_id=None, peg_vigente=True):
        self.peg_id = peg_id
        self.gru_id = gru_id
        self.per_id = per_id
        self.peg_vigente = peg_vigente

    def __str__(self):
        return f"{self.per_id} en {self.gru_id}"

class PersonaNivel:
    def __init__(self, pen_id=1, per_id=None, niv_id=None, ram_id=None):
        self.pen_id = pen_id
        self.per_id = per_id
        self.niv_id = niv_id
        self.ram_id = ram_id

    def __str__(self):
        return f"{self.per_id} - {self.niv_id} ({self.ram_id})"

class PersonaFormador:
    def __init__(self, pef_id=1, per_id=None, pef_hab_1=False, pef_hab_2=False, pef_verif=False, pef_historial="Ninguno"):
        self.pef_id = pef_id
        self.per_id = per_id
        self.pef_hab_1 = pef_hab_1
        self.pef_hab_2 = pef_hab_2
        self.pef_verif = pef_verif
        self.pef_historial = pef_historial

    def __str__(self):
        return f"Formador: {self.per_id}"

class PersonaIndividual:
    def __init__(self, pei_id=1, per_id=None, car_id=None, dis_id=None, zon_id=None, pei_vigente=True):
        self.pei_id = pei_id
        self.per_id = per_id
        self.car_id = car_id
        self.dis_id = dis_id
        self.zon_id = zon_id
        self.pei_vigente = pei_vigente

    def __str__(self):
        return f"Individual: {self.per_id} - Cargo: {self.car_id}"

class PersonaVehiculo:
    def __init__(self, pev_id=1, per_id=None, pev_marca="Toyota", pev_modelo="Corolla", pev_patente="AB1234"):
        self.pev_id = pev_id
        self.per_id = per_id
        self.pev_marca = pev_marca
        self.pev_modelo = pev_modelo
        self.pev_patente = pev_patente

    def __str__(self):
        return f"{self.pev_marca} {self.pev_modelo} ({self.pev_patente})"

# --- Actual Test Cases ---

def test_persona_creation():
    persona = Persona(
        esc_id=mock_estado_civil,
        com_id=mock_comuna,
        usu_id=mock_usuario,
        per_run=12345678,
        per_dv="9",
        per_apelpat="Perez",
        per_nombres="Juan",
        per_email="juan.perez@example.com",
        per_fecha_nac=timezone.datetime(1990, 5, 15),
        per_direccion="Calle Falsa 123",
        per_fono="987654321",
        per_nom_emergencia="Maria",
        per_fono_emergencia="11223344",
        per_num_mmaa=2,
        per_profesion="Ingeniero",
        per_apodo="Juanito",
        per_vigente=True
    )
    assert isinstance(persona, Persona)
    assert persona.per_run == 12345678
    assert persona.per_dv == "9"
    assert persona.per_apelpat == "Perez"
    assert persona.per_nombres == "Juan"
    assert persona.per_email == "juan.perez@example.com"
    assert persona.per_direccion == "Calle Falsa 123"
    assert persona.per_fono == "987654321"
    assert persona.per_nom_emergencia == "Maria"
    assert persona.per_fono_emergencia == "11223344"
    assert persona.per_num_mmaa == 2
    assert persona.per_profesion == "Ingeniero"
    assert persona.per_apodo == "Juanito"
    assert persona.per_vigente == True
    assert persona.esc_id == mock_estado_civil
    assert persona.com_id == mock_comuna
    assert persona.usu_id == mock_usuario
    assert str(persona) == "Juan Perez"

def test_personagrupo_creation():
    persona_grupo = PersonaGrupo(gru_id=mock_grupo, per_id=mock_usuario, peg_vigente=True)
    assert isinstance(persona_grupo, PersonaGrupo)
    assert persona_grupo.gru_id == mock_grupo
    assert persona_grupo.per_id == mock_usuario
    assert persona_grupo.peg_vigente == True
    assert str(persona_grupo) == f"{mock_usuario} en {mock_grupo}"

def test_personanivel_creation():
    persona_nivel = PersonaNivel(per_id=mock_usuario, niv_id=mock_nivel, ram_id=mock_rama)
    assert isinstance(persona_nivel, PersonaNivel)
    assert persona_nivel.per_id == mock_usuario
    assert persona_nivel.niv_id == mock_nivel
    assert persona_nivel.ram_id == mock_rama
    assert str(persona_nivel) == f"{mock_usuario} - {mock_nivel} ({mock_rama})"

def test_personaformador_creation():
    persona_formador = PersonaFormador(per_id=mock_usuario, pef_hab_1=True, pef_hab_2=False, pef_verif=True, pef_historial="Capacitación en metodologías ágiles")
    assert isinstance(persona_formador, PersonaFormador)
    assert persona_formador.per_id == mock_usuario
    assert persona_formador.pef_hab_1 == True
    assert persona_formador.pef_hab_2 == False
    assert persona_formador.pef_verif == True
    assert persona_formador.pef_historial == "Capacitación en metodologías ágiles"
    assert str(persona_formador) == f"Formador: {mock_usuario}"

def test_personaindividual_creation():
    persona_individual = PersonaIndividual(per_id=mock_usuario, car_id=mock_cargo, dis_id=mock_distrito, zon_id=mock_zona, pei_vigente=True)
    assert isinstance(persona_individual, PersonaIndividual)
    assert persona_individual.per_id == mock_usuario
    assert persona_individual.car_id == mock_cargo
    assert persona_individual.dis_id == mock_distrito
    assert persona_individual.zon_id == mock_zona
    assert persona_individual.pei_vigente == True
    assert str(persona_individual) == f"Individual: {mock_usuario} - Cargo: {mock_cargo}"

def test_personavehiculo_creation():
    persona_vehiculo = PersonaVehiculo(per_id=mock_usuario, pev_marca="Ford", pev_modelo="Fiesta", pev_patente="CD5678")
    assert isinstance(persona_vehiculo, PersonaVehiculo)
    assert persona_vehiculo.per_id == mock_usuario
    assert persona_vehiculo.pev_marca == "Ford"
    assert persona_vehiculo.pev_modelo == "Fiesta"
    assert persona_vehiculo.pev_patente == "CD5678"
    assert str(persona_vehiculo) == "Ford Fiesta (CD5678)"

# Note: In a real Django project, you would import the actual models like:
# from ..models import Persona, PersonaGrupo, PersonaNivel, PersonaFormador, PersonaIndividual, PersonaVehiculo
# And use Django's test client and database for more robust testing.
# The mocks are used here to simulate model creation without a full Django setup.
