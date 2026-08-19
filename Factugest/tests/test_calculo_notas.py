"""Pruebas de la aritmética de las notas.

Una nota crédito devuelve dinero y una nota débito lo cobra: son las dos
operaciones donde un redondeo mal puesto se convierte en una diferencia a favor o
en contra de alguien. Como no tocan base de datos, se prueban aquí completas.
"""
import pytest

from services.calculo_documento import (calcular_documento, calcular_nota_credito,
                                        calcular_nota_debito, tasa_promedio)


def factura_de_prueba():
    """Tres teclados con 10 % de descuento y un mouse, todo al 19 %."""
    return calcular_documento([
        {"codigo": "A-1", "descripcion": "Teclado", "cantidad": 3,
         "precio_unitario": 100000, "descuento_porcentaje": 10,
         "impuesto_porcentaje": 19},
        {"codigo": "A-2", "descripcion": "Mouse", "cantidad": 1,
         "precio_unitario": 50000, "impuesto_porcentaje": 19},
    ])


# ── Nota crédito ────────────────────────────────────────────────────────────

def test_la_anulacion_total_devuelve_exactamente_lo_facturado():
    factura = factura_de_prueba()
    nota = calcular_nota_credito(factura["lineas"])

    assert nota["subtotal"] == factura["subtotal"]
    assert nota["total_impuestos"] == factura["total_impuestos"]
    assert nota["total"] == factura["total"]
    assert len(nota["lineas"]) == len(factura["lineas"])


def test_los_importes_de_la_nota_son_positivos():
    """El signo lo lleva el tipo del documento, no los números.

    En negativo habría que poner un `abs()` en cada sitio que la muestre, y el XML
    saldría con cantidades que la DIAN no admite."""
    nota = calcular_nota_credito(factura_de_prueba()["lineas"])
    assert nota["total"] > 0
    assert all(l["subtotal"] > 0 for l in nota["lineas"])


def test_la_devolucion_parcial_prorratea_base_descuento_e_impuesto():
    factura = factura_de_prueba()
    nota = calcular_nota_credito(factura["lineas"], {1: 1})

    assert len(nota["lineas"]) == 1
    linea = nota["lineas"][0]
    # Un tercio de la línea: bruto 300.000, descuento 30.000, base 270.000.
    assert linea["valor_bruto"] == 100000
    assert linea["descuento_valor"] == 10000
    assert linea["subtotal"] == 90000
    assert linea["impuesto_valor"] == 17100
    assert nota["total"] == 107100


def test_devolver_sin_prorratear_el_descuento_regresaria_de_mas():
    """El caso que justifica el prorrateo: sin él volverían 100.000 de base."""
    nota = calcular_nota_credito(factura_de_prueba()["lineas"], {1: 1})
    assert nota["lineas"][0]["subtotal"] < 100000


def test_una_linea_no_devuelta_no_entra_en_la_nota():
    nota = calcular_nota_credito(factura_de_prueba()["lineas"], {2: 1})
    assert [l["codigo"] for l in nota["lineas"]] == ["A-2"]


def test_devolver_cero_deja_la_nota_vacia():
    nota = calcular_nota_credito(factura_de_prueba()["lineas"], {1: 0})
    assert nota["lineas"] == []
    assert nota["total"] == 0


def test_la_nota_conserva_el_orden_de_la_linea_original():
    """Es lo que permite acumular devoluciones sin devolver de más."""
    nota = calcular_nota_credito(factura_de_prueba()["lineas"], {2: 1})
    assert nota["lineas"][0]["orden"] == 2


# ── Nota débito ─────────────────────────────────────────────────────────────

def test_el_valor_con_iva_adentro_se_descompone():
    nota = calcular_nota_debito(50000, 19, incluye_impuesto=True)
    assert nota["subtotal"] == 42016.81
    assert nota["total_impuestos"] == 7983.19
    # Lo que paga el comprador es exactamente lo que se pidió cobrar.
    assert nota["total"] == 50000


def test_el_valor_sin_iva_lo_suma_encima():
    nota = calcular_nota_debito(50000, 19, incluye_impuesto=False)
    assert nota["subtotal"] == 50000
    assert nota["total_impuestos"] == 9500
    assert nota["total"] == 59500


def test_las_dos_formas_no_dan_lo_mismo():
    """Por eso el que integra tiene que decir cuál está pidiendo."""
    con = calcular_nota_debito(50000, 19, incluye_impuesto=True)
    sin = calcular_nota_debito(50000, 19, incluye_impuesto=False)
    assert con["total"] != sin["total"]


def test_un_ajuste_sin_impuesto_no_inventa_iva():
    nota = calcular_nota_debito(50000, 0, incluye_impuesto=True)
    assert nota["total_impuestos"] == 0
    assert nota["total"] == 50000


# ── Tarifa promedio ─────────────────────────────────────────────────────────

def test_la_tarifa_promedio_de_un_documento_de_una_sola_tarifa_es_esa_tarifa():
    factura = factura_de_prueba()
    assert tasa_promedio(factura["subtotal"], factura["total_impuestos"]) == 19.0


def test_la_tarifa_promedio_de_un_documento_mixto_queda_en_medio():
    mixta = calcular_documento([
        {"cantidad": 1, "precio_unitario": 100000, "impuesto_porcentaje": 19},
        {"cantidad": 1, "precio_unitario": 100000, "impuesto_porcentaje": 0},
    ])
    assert 0 < tasa_promedio(mixta["subtotal"], mixta["total_impuestos"]) < 19


@pytest.mark.parametrize("subtotal", [0, None, -5])
def test_un_documento_sin_base_no_divide_por_cero(subtotal):
    assert tasa_promedio(subtotal, 1000) == 0.0
