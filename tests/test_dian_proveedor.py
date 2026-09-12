"""
Pruebas del adaptador de proveedor DIAN.

Valen doble: comprueban el simulador y, al mismo tiempo, dejan escrito el
contrato que tendrá que cumplir el proveedor real de la fase 7.
"""
import pytest

from services.dian_proveedor import (ACEPTADO, RECHAZADO, ErrorProveedorDian,
                                     ProveedorSimulado, get_proveedor,
                                     proveedores_disponibles)

CUFE = "a" * 96   # un SHA-384 en hexadecimal son 96 caracteres

XML_OK = "<?xml version='1.0' encoding='UTF-8'?><Invoice><ID>SETP1</ID></Invoice>"


def cabecera(**cambios):
    base = {
        "numero_factura": "SETP1",
        "cufe": CUFE,
        "document_number": "1090234567",
        "subtotal": 100000.0,
        "total_impuestos": 19000.0,
        "total": 119000.0,
    }
    base.update(cambios)
    return base


def lineas(**cambios):
    base = {"subtotal": 100000.0, "impuesto_valor": 19000.0}
    base.update(cambios)
    return [base]


EMISOR = {"nit": "901555444", "nombre": "Siste Soluciones S.A.S."}


def transmitir(cab=None, lin=None, emisor=EMISOR, xml=XML_OK):
    return ProveedorSimulado().transmitir(
        cab if cab is not None else cabecera(),
        lin if lin is not None else lineas(),
        emisor, xml)


# ── Camino feliz ────────────────────────────────────────────────────────────

def test_un_documento_coherente_se_acepta():
    r = transmitir()
    assert r.aceptado is True
    assert r.estado == ACEPTADO
    assert r.codigo == "00"
    assert r.proveedor == "simulado"


def test_la_respuesta_trae_el_qr_del_catalogo_de_habilitacion():
    r = transmitir()
    assert r.qr.endswith(CUFE)
    # Habilitación, no producción: el CUFE se calcula con tipAmbiente = 2.
    assert "vpfe-hab" in r.qr


def test_el_acuse_es_reproducible_para_el_mismo_documento():
    """Repetir una prueba tiene que dar el mismo resultado."""
    assert transmitir().payload["acuse"] == transmitir().payload["acuse"]
    otro = transmitir(cabecera(cufe="b" * 96))
    assert otro.payload["acuse"] != transmitir().payload["acuse"]


def test_el_payload_avisa_que_no_hubo_transmision_real():
    """Queda en documento_eventos: nadie debería creer que esto llegó a la DIAN."""
    assert "no transmitido" in transmitir().payload["advertencia"].lower()


def test_el_simulador_no_inventa_numero_ni_cufe_ni_pdf():
    """Los genera FactuGest. Un proveedor real sí puede devolver los suyos."""
    r = transmitir()
    assert r.numero is None and r.cufe is None and r.pdf is None and r.xml is None


# ── Rechazos ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("cambio,esperado", [
    ({"numero_factura": ""}, "no tiene número"),
    ({"cufe": ""}, "no tiene CUFE"),
    ({"cufe": "abc123"}, "forma de un SHA-384"),
    ({"cufe": "z" * 96}, "forma de un SHA-384"),
    ({"document_number": ""}, "receptor no está identificado"),
])
def test_se_rechaza_lo_que_la_dian_rechazaria(cambio, esperado):
    r = transmitir(cabecera(**cambio))
    assert r.aceptado is False
    assert r.estado == RECHAZADO
    assert esperado in r.mensaje


def test_se_rechaza_un_emisor_sin_nit():
    r = transmitir(emisor={"nombre": "Sin NIT"})
    assert not r.aceptado and "emisor no tiene NIT" in r.mensaje


def test_se_rechaza_un_documento_sin_lineas():
    r = transmitir(lin=[])
    assert not r.aceptado and "no tiene líneas" in r.mensaje


def test_se_rechaza_un_total_que_no_cuadra():
    r = transmitir(cabecera(total=999999.0))
    assert not r.aceptado and "no corresponde a la base más los impuestos" in r.mensaje


def test_se_rechaza_un_iva_mayor_que_el_de_las_lineas():
    r = transmitir(cabecera(total_impuestos=50000.0, total=150000.0),
                   lineas(impuesto_valor=19000.0))
    assert not r.aceptado and "superan la suma" in r.mensaje


def test_se_rechaza_un_xml_mal_formado():
    r = transmitir(xml="<Invoice><ID>sin cerrar")
    assert not r.aceptado and "bien formado" in r.mensaje


def test_se_rechaza_si_no_se_genero_el_xml():
    r = transmitir(xml="")
    assert not r.aceptado and "no se generó el XML" in r.mensaje


def test_se_informan_todos_los_problemas_de_una_vez():
    r = transmitir(cabecera(numero_factura="", cufe=""), lin=[], emisor={})
    assert r.mensaje.count(";") >= 3
    assert len(r.payload["problemas"]) >= 4


def test_un_rechazo_no_lanza_excepcion():
    """Rechazado es una respuesta, no un fallo: el documento llegó y no pasó."""
    r = transmitir(cabecera(cufe=""))
    assert r.estado == RECHAZADO


# ── Una nota crédito lleva los valores en negativo ───────────────────────────

def test_una_nota_credito_con_valores_negativos_se_acepta():
    r = transmitir(
        cabecera(subtotal=-100000.0, total_impuestos=-19000.0, total=-119000.0),
        lineas(subtotal=-100000.0, impuesto_valor=-19000.0))
    assert r.aceptado, r.mensaje


# ── Selección del proveedor ─────────────────────────────────────────────────

def test_por_defecto_se_usa_el_simulado(monkeypatch):
    monkeypatch.delenv("DIAN_PROVEEDOR", raising=False)
    assert get_proveedor().nombre == "simulado"


def test_la_variable_de_entorno_elige_el_proveedor(monkeypatch):
    monkeypatch.setenv("DIAN_PROVEEDOR", "SIMULADO")
    assert get_proveedor().nombre == "simulado"


def test_factus_avisa_que_esta_pendiente_en_lugar_de_decir_desconocido():
    with pytest.raises(ErrorProveedorDian) as e:
        get_proveedor("factus")
    assert "7.2" in str(e.value)


def test_un_proveedor_inventado_lista_los_disponibles():
    with pytest.raises(ErrorProveedorDian) as e:
        get_proveedor("dian_directo")
    assert "simulado" in str(e.value)


def test_los_disponibles_se_pueden_consultar():
    assert proveedores_disponibles() == ["simulado"]
