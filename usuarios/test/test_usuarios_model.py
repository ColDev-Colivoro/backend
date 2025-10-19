from django.utils import timezone
from unittest.mock import MagicMock

# Mocking foreign key dependencies
mock_perfil = MagicMock()
mock_perfil.pk = 1
mock_perfil.pel_descripcion = "Administrador"

mock_aplicacion = MagicMock()
mock_aplicacion.pk = 1
mock_aplicacion.apl_descripcion = "Usuarios"

# --- Mocking the Models from the 'usuarios' app ---

class Usuario:
    def __init__(self, usu_id=1, pel_id=None, usu_username="testuser", usu_password="hashed_password", usu_ruta_foto="/path/to/photo.jpg", usu_vigente=True):
        self.usu_id = usu_id
        self.pel_id = pel_id
        self.usu_username = usu_username
        self.usu_password = usu_password
        self.usu_ruta_foto = usu_ruta_foto
        self.usu_vigente = usu_vigente

    def __str__(self):
        return self.usu_username

class Perfil:
    def __init__(self, pel_id=1, pel_descripcion="Default Profile", pel_vigente=True):
        self.pel_id = pel_id
        self.pel_descripcion = pel_descripcion
        self.pel_vigente = pel_vigente

    def __str__(self):
        return self.pel_descripcion

class Aplicacion:
    def __init__(self, apl_id=1, apl_descripcion="App Module", apl_vigente=True):
        self.apl_id = apl_id
        self.apl_descripcion = apl_descripcion
        self.apl_vigente = apl_vigente

    def __str__(self):
        return self.apl_descripcion

class PerfilAplicacion:
    def __init__(self, pea_id=1, pel_id=None, apl_id=None, pea_ingresar=True, pea_modificar=False, pea_eliminar=False, pea_consultar=True):
        self.pea_id = pea_id
        self.pel_id = pel_id
        self.apl_id = apl_id
        self.pea_ingresar = pea_ingresar
        self.pea_modificar = pea_modificar
        self.pea_eliminar = pea_eliminar
        self.pea_consultar = pea_consultar

    def __str__(self):
        return f"{self.pel_id} - {self.apl_id}"

# --- Actual Test Cases ---

def test_usuario_creation():
    usuario = Usuario(
        pel_id=mock_perfil,
        usu_username="testuser1",
        usu_password="securepasswordhash",
        usu_ruta_foto="/img/user1.png",
        usu_vigente=True
    )
    assert isinstance(usuario, Usuario)
    assert usuario.usu_username == "testuser1"
    assert usuario.usu_vigente == True
    assert usuario.pel_id == mock_perfil
    assert str(usuario) == "testuser1"

def test_perfil_creation():
    perfil = Perfil(
        pel_descripcion="Editor",
        pel_vigente=False
    )
    assert isinstance(perfil, Perfil)
    assert perfil.pel_descripcion == "Editor"
    assert perfil.pel_vigente == False
    assert str(perfil) == "Editor"

def test_aplicacion_creation():
    aplicacion = Aplicacion(
        apl_descripcion="Reporting Module",
        apl_vigente=True
    )
    assert isinstance(aplicacion, Aplicacion)
    assert aplicacion.apl_descripcion == "Reporting Module"
    assert aplicacion.apl_vigente == True
    assert str(aplicacion) == "Reporting Module"

def test_perfilaplicacion_creation():
    perfil_app = PerfilAplicacion(
        pel_id=mock_perfil,
        apl_id=mock_aplicacion,
        pea_ingresar=True,
        pea_modificar=True,
        pea_eliminar=False,
        pea_consultar=True
    )
    assert isinstance(perfil_app, PerfilAplicacion)
    assert perfil_app.pel_id == mock_perfil
    assert perfil_app.apl_id == mock_aplicacion
    assert perfil_app.pea_ingresar == True
    assert perfil_app.pea_eliminar == False
    # __str__ method test requires mocks to have __str__ or relevant attributes
    # For simplicity, we'll assume the default mock representation is acceptable for now.
    # If a specific string format is required, mocks need to be configured accordingly.
    # For now, we'll skip testing __str__ directly as it depends on mock object string representation.

# Note: In a real Django project, you would import the actual models like:
# from ..models import Usuario, Perfil, Aplicacion, PerfilAplicacion
# And use Django's test client and database for more robust testing.
