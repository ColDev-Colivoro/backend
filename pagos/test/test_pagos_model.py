from django.test import TestCase
from django.utils import timezone
from unittest.mock import MagicMock

# Mocking foreign key dependencies
mock_persona = MagicMock()
mock_persona.pk = 1
mock_persona.per_nombres = "Juan"
mock_persona.per_apelpat = "Perez"

mock_curso = MagicMock()
mock_curso.pk = 1
mock_curso.cur_codigo = "C101"
mock_curso.cur_descripcion = "Curso de Prueba"

mock_usuario = MagicMock()
mock_usuario.pk = 1
mock_usuario.usu_username = "test_user"

mock_persona_curso = MagicMock()
mock_persona_curso.pk = 1

mock_concepto_contable = MagicMock()
mock_concepto_contable.pk = 1
mock_concepto_contable.coc_descripcion = "Matricula"

# --- Mocking the Models from the 'pagos' app ---

class PagoPersona:
    def __init__(self, pap_id=1, per_id=None, cur_id=None, usu_id=None, pap_fecha_hora=None, pap_tipo=1, pap_valor=100.0, pap_observacion="Pago inicial"):
        self.pap_id = pap_id
        self.per_id = per_id
        self.cur_id = cur_id
        self.usu_id = usu_id
        self.pap_fecha_hora = pap_fecha_hora if pap_fecha_hora else timezone.now()
        self.pap_tipo = pap_tipo
        self.pap_valor = pap_valor
        self.pap_observacion = pap_observacion

    def __str__(self):
        return f"Pago {self.pap_id} de {self.per_id} por {self.pap_valor}"

class ComprobantePago:
    def __init__(self, cpa_id=1, usu_id=None, pec_id=None, coc_id=None, cpa_fecha_hora=None, cpa_fecha=None, cpa_numero=1001, cpa_valor=100.0):
        self.cpa_id = cpa_id
        self.usu_id = usu_id
        self.pec_id = pec_id
        self.coc_id = coc_id
        self.cpa_fecha_hora = cpa_fecha_hora if cpa_fecha_hora else timezone.now()
        self.cpa_fecha = cpa_fecha if cpa_fecha else timezone.now().date()
        self.cpa_numero = cpa_numero
        self.cpa_valor = cpa_valor

    def __str__(self):
        return f"Comprobante {self.cpa_numero} ({self.cpa_valor})"

class PagoComprobante:
    def __init__(self, pco_id=1, pap_id=None, cpa_id=None):
        self.pco_id = pco_id
        self.pap_id = pap_id
        self.cpa_id = cpa_id

    def __str__(self):
        return f"Pago {self.pap_id} con Comprobante {self.cpa_id}"

class PagoCambioPersona:
    def __init__(self, pcp_id=1, per_id=None, pap_id=None, usu_id=None, pcp_fecha_hora=None):
        self.pcp_id = pcp_id
        self.per_id = per_id
        self.pap_id = pap_id
        self.usu_id = usu_id
        self.pcp_fecha_hora = pcp_fecha_hora if pcp_fecha_hora else timezone.now()

    def __str__(self):
        return f"Cambio en pago {self.pap_id} para {self.per_id} por {self.usu_id}"

class Prepago:
    def __init__(self, ppa_id=1, per_id=None, cur_id=None, pap_id=None, ppa_valor=50.0, ppa_observacion="Prepago para materiales", ppa_vigente=True):
        self.ppa_id = ppa_id
        self.per_id = per_id
        self.cur_id = cur_id
        self.pap_id = pap_id
        self.ppa_valor = ppa_valor
        self.ppa_observacion = ppa_observacion
        self.ppa_vigente = ppa_vigente

    def __str__(self):
        return f"Prepago {self.ppa_id} de {self.per_id} por {self.ppa_valor} para {self.cur_id}"

# --- Actual Test Cases ---

class PagoPersonaModelTests(TestCase):
    def setUp(self):
        self.mock_persona = mock_persona
        self.mock_curso = mock_curso
        self.mock_usuario = mock_usuario

    def test_pago_persona_creation(self):
        pago_persona = PagoPersona(
            per_id=self.mock_persona,
            cur_id=self.mock_curso,
            usu_id=self.mock_usuario,
            pap_tipo=1, # Ingreso
            pap_valor=150.0,
            pap_observacion="Pago de matrícula"
        )
        self.assertIsInstance(pago_persona, PagoPersona)
        self.assertEqual(pago_persona.per_id, self.mock_persona)
        self.assertEqual(pago_persona.cur_id, self.mock_curso)
        self.assertEqual(pago_persona.usu_id, self.mock_usuario)
        self.assertEqual(pago_persona.pap_tipo, 1)
        self.assertEqual(pago_persona.pap_valor, 150.0)
        self.assertEqual(pago_persona.pap_observacion, "Pago de matrícula")
        self.assertIsNotNone(pago_persona.pap_fecha_hora)
        self.assertEqual(str(pago_persona), f"Pago {pago_persona.pap_id} de {self.mock_persona} por {pago_persona.pap_valor}")

class ComprobantePagoModelTests(TestCase):
    def setUp(self):
        self.mock_usuario = mock_usuario
        self.mock_persona_curso = mock_persona_curso
        self.mock_concepto_contable = mock_concepto_contable

    def test_comprobante_pago_creation(self):
        fecha_comprobante = timezone.datetime(2023, 10, 26).date()
        comprobante_pago = ComprobantePago(
            usu_id=self.mock_usuario,
            pec_id=self.mock_persona_curso,
            coc_id=self.mock_concepto_contable,
            cpa_fecha=fecha_comprobante,
            cpa_numero=1005,
            cpa_valor=150.0
        )
        self.assertIsInstance(comprobante_pago, ComprobantePago)
        self.assertEqual(comprobante_pago.usu_id, self.mock_usuario)
        self.assertEqual(comprobante_pago.pec_id, self.mock_persona_curso)
        self.assertEqual(comprobante_pago.coc_id, self.mock_concepto_contable)
        self.assertEqual(comprobante_pago.cpa_fecha, fecha_comprobante)
        self.assertEqual(comprobante_pago.cpa_numero, 1005)
        self.assertEqual(comprobante_pago.cpa_valor, 150.0)
        self.assertIsNotNone(comprobante_pago.cpa_fecha_hora)
        self.assertEqual(str(comprobante_pago), f"Comprobante {comprobante_pago.cpa_numero} ({comprobante_pago.cpa_valor})")

class PagoComprobanteModelTests(TestCase):
    def setUp(self):
        self.mock_pago_persona = MagicMock()
        self.mock_pago_persona.pk = 5
        self.mock_pago_persona.__str__.return_value = "Mock PagoPersona String"

        self.mock_comprobante_pago = MagicMock()
        self.mock_comprobante_pago.pk = 10
        self.mock_comprobante_pago.__str__.return_value = "Mock ComprobantePago String"

    def test_pago_comprobante_creation(self):
        pago_comprobante = PagoComprobante(pap_id=self.mock_pago_persona, cpa_id=self.mock_comprobante_pago)
        self.assertIsInstance(pago_comprobante, PagoComprobante)
        self.assertEqual(pago_comprobante.pap_id, self.mock_pago_persona)
        self.assertEqual(pago_comprobante.cpa_id, self.mock_comprobante_pago)
        self.assertEqual(str(pago_comprobante), f"Pago {self.mock_pago_persona} con Comprobante {self.mock_comprobante_pago}")

class PagoCambioPersonaModelTests(TestCase):
    def setUp(self):
        self.mock_persona = mock_persona # Reusing mock_persona
        self.mock_pago_persona = MagicMock()
        self.mock_pago_persona.pk = 5
        self.mock_usuario = mock_usuario

    def test_pago_cambio_persona_creation(self):
        pago_cambio = PagoCambioPersona(per_id=self.mock_persona, pap_id=self.mock_pago_persona, usu_id=self.mock_usuario)
        self.assertIsInstance(pago_cambio, PagoCambioPersona)
        self.assertEqual(pago_cambio.per_id, self.mock_persona)
        self.assertEqual(pago_cambio.pap_id, self.mock_pago_persona)
        self.assertEqual(pago_cambio.usu_id, self.mock_usuario)
        self.assertIsNotNone(pago_cambio.pcp_fecha_hora)
        self.assertEqual(str(pago_cambio), f"Cambio en pago {self.mock_pago_persona} para {self.mock_persona} por {self.mock_usuario}")

class PrepagoModelTests(TestCase):
    def setUp(self):
        self.mock_persona = mock_persona # Reusing mock_persona
        self.mock_curso = mock_curso # Reusing mock_curso
        self.mock_pago_persona = MagicMock()
        self.mock_pago_persona.pk = 5

    def test_prepago_creation(self):
        prepago = Prepago(
            per_id=self.mock_persona,
            cur_id=self.mock_curso,
            pap_id=self.mock_pago_persona,
            ppa_valor=75.0,
            ppa_observacion="Prepago para materiales y uniforme",
            ppa_vigente=False
        )
        self.assertIsInstance(prepago, Prepago)
        self.assertEqual(prepago.per_id, self.mock_persona)
        self.assertEqual(prepago.cur_id, self.mock_curso)
        self.assertEqual(prepago.pap_id, self.mock_pago_persona)
        self.assertEqual(prepago.ppa_valor, 75.0)
        self.assertEqual(prepago.ppa_observacion, "Prepago para materiales y uniforme")
        self.assertFalse(prepago.ppa_vigente)
        self.assertEqual(str(prepago), f"Prepago {prepago.ppa_id} de {self.mock_persona} por {prepago.ppa_valor} para {self.mock_curso}")

# Note: In a real Django project, you would import the actual models like:
# from ..models import PagoPersona, ComprobantePago, PagoComprobante, PagoCambioPersona, Prepago
# And use Django's test client and database for more robust testing.
# The mocks are used here to simulate model creation without a full Django setup.
