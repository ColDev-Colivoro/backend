from django.test import TestCase
from unittest.mock import MagicMock

# Mocking foreign key dependencies
mock_usuario = MagicMock()
mock_usuario.pk = 1
mock_usuario.usu_username = "test_user"

mock_comuna = MagicMock()
mock_comuna.pk = 1
mock_comuna.com_descripcion = "Santiago Centro"

# --- Mocking the Models from the 'proveedores' app ---

class Proveedor:
    def __init__(self, pro_id=1, usu_id=None, com_id=None, pro_fecha_hora=None, pro_rut="76.123.456-7", pro_razon_social="Proveedor XYZ", pro_nombre_contacto="Juan Perez", pro_email="proveedor@example.com", pro_fono="55512345", pro_direccion="Av. Siempre Viva 742", pro_vigente=True):
        self.pro_id = pro_id
        self.usu_id = usu_id
        self.com_id = com_id
        self.pro_fecha_hora = pro_fecha_hora if pro_fecha_hora else timezone.now()
        self.pro_rut = pro_rut
        self.pro_razon_social = pro_razon_social
        self.pro_nombre_contacto = pro_nombre_contacto
        self.pro_email = pro_email
        self.pro_fono = pro_fono
        self.pro_direccion = pro_direccion
        self.pro_vigente = pro_vigente

    def __str__(self):
        return f"{self.pro_razon_social} ({self.pro_rut})"

# --- Actual Test Cases ---

class ProveedorModelTests(TestCase):
    def setUp(self):
        self.mock_usuario = mock_usuario
        self.mock_comuna = mock_comuna

    def test_proveedor_creation(self):
        proveedor = Proveedor(
            usu_id=self.mock_usuario,
            com_id=self.mock_comuna,
            pro_rut="761234567", # RUT without hyphen and digit for simplicity in mock
            pro_razon_social="Proveedor ABC Ltda.",
            pro_nombre_contacto="Ana Lopez",
            pro_email="ana.lopez@proveedorabc.com",
            pro_fono="55598765",
            pro_direccion="Calle Falsa 456",
            pro_vigente=True
        )
        self.assertIsInstance(proveedor, Proveedor)
        self.assertEqual(proveedor.pro_rut, "761234567")
        self.assertEqual(proveedor.pro_razon_social, "Proveedor ABC Ltda.")
        self.assertEqual(proveedor.pro_nombre_contacto, "Ana Lopez")
        self.assertEqual(proveedor.pro_email, "ana.lopez@proveedorabc.com")
        self.assertEqual(proveedor.pro_fono, "55598765")
        self.assertEqual(proveedor.pro_direccion, "Calle Falsa 456")
        self.assertTrue(proveedor.pro_vigente)
        self.assertEqual(proveedor.usu_id, self.mock_usuario)
        self.assertEqual(proveedor.com_id, self.mock_comuna)
        self.assertIsNotNone(proveedor.pro_fecha_hora)
        self.assertEqual(str(proveedor), "Proveedor ABC Ltda. (761234567)")

# Note: In a real Django project, you would import the actual models like:
# from ..models import Proveedor
# And use Django's test client and database for more robust testing.
# The mocks are used here to simulate model creation without a full Django setup.
