"""Cómo se muestran los descuentos en el pie de la factura.

El defecto que motivó estas pruebas: la fila decía «(-) Descuentos (0.0%)» junto a
un importe real de −$657.000. Sumaba los descuentos de línea con el de factura en
una sola fila, pero la rotulaba con el porcentaje del descuento **de factura**;
cuando la rebaja venía de las líneas —el caso corriente— ese porcentaje era cero.

Un documento fiscal que muestra un descuento del 0 % restando dinero es un
documento que no se puede explicar. Aquí se fija que cada descuento salga con su
base y su nombre.
"""
import io

import pytest

from services.pdf_service import generate_invoice_pdf

pypdf = pytest.importorskip("pypdf", reason="pypdf solo se usa para leer el PDF de vuelta")

EMISOR = {
    "nombre": "Drogueria La Salud S.A.S.", "nit": "900874512", "dv": "3",
    "direccion": "Calle 11 # 6-32", "ciudad": "San Jose De Cucuta",
    "telefono": "6075742210", "correo": "administracion@lasalud.co",
    "regimen_tributario": "RESPONSABLE_IVA", "actividad_economica": "4772",
    "prefijo_factura": "DLS", "resolucion_dian": "18764003812501",
    "resolucion_fecha_desde": "2026-01-01", "resolucion_fecha_hasta": "2026-12-31",
    "resolucion_desde": 1, "resolucion_hasta": 20000,
    "tarifa_ica": 0, "autoretenedor": 0, "gran_contribuyente": 0,
    "website": "", "logo": None, "color_marca": "#7a0000",
}

CABECERA = {
    "numero_factura": "DLS9", "tipo_factura": "FV", "fecha": "2026-08-01 10:00:00",
    "cufe": "a" * 96, "forma_pago": "CONTADO", "cliente_nombre": "Ana Maria Rodriguez",
    "document_type": "13", "document_number": "1090123456",
}


def linea(**cambios):
    base = {
        "producto_nombre": "Suero fisiologico 500 ml", "sku": "SUE-01",
        "unidad_medida": "94", "cantidad": 1, "precio_unitario": 3000000,
        "subtotal": 3000000, "descuento_porcentaje": 0, "descuento_valor": 0,
        "descripcion_descuento": None, "impuesto_porcentaje": 19,
        "impuesto_valor": 570000,
    }
    base.update(cambios)
    return base


def texto(cabecera, lineas):
    pdf = generate_invoice_pdf(cabecera, lineas, emisor=EMISOR)
    lector = pypdf.PdfReader(io.BytesIO(pdf))
    return " ".join(" ".join((p.extract_text() or "").split()) for p in lector.pages)


CON_DESCUENTO_DE_LINEA = [linea(subtotal=2700000, descuento_porcentaje=10,
                                descuento_valor=300000,
                                descripcion_descuento="Convenio empresarial",
                                impuesto_valor=513000)]


def test_el_descuento_por_producto_sale_con_su_porcentaje_real():
    """Era el caso roto: importe correcto, porcentaje en 0,0 %."""
    t = texto(dict(CABECERA, subtotal=2700000, total_descuentos=300000,
                   total_impuestos=513000, total=3213000),
              CON_DESCUENTO_DE_LINEA)

    assert "Dto. por producto (10.0%)" in t
    assert "(0.0%)" not in t


def test_el_descuento_de_factura_sale_con_su_concepto():
    """Es el que no tiene sitio en la tabla de líneas: si no sale aquí, no sale."""
    t = texto(dict(CABECERA, subtotal=2565000, total_descuentos=435000,
                   total_impuestos=487350, total=3052350,
                   descripcion_descuento_factura="Promocion de temporada"),
              CON_DESCUENTO_DE_LINEA)

    assert "Dto. de factura: Promocion de temporada (5.0%)" in t


def test_los_dos_descuentos_salen_en_filas_distintas():
    """Sumarlos en una sola fila obliga a adivinar de dónde salió cada peso."""
    t = texto(dict(CABECERA, subtotal=2565000, total_descuentos=435000,
                   total_impuestos=487350, total=3052350,
                   descripcion_descuento_factura="Promocion de temporada"),
              CON_DESCUENTO_DE_LINEA)

    assert "Dto. por producto (10.0%)" in t
    assert "Dto. de factura" in t
    assert "-$ 300,000.00" in t
    assert "-$ 135,000.00" in t


def test_el_de_factura_se_calcula_sobre_lo_que_queda_del_de_linea():
    """Es el orden en que los aplica `calculo_documento`: primero la línea, y el de
    factura sobre el neto. Sobre el bruto daría 4,5 % y no el 5 % pactado."""
    t = texto(dict(CABECERA, subtotal=2565000, total_descuentos=435000,
                   total_impuestos=487350, total=3052350),
              CON_DESCUENTO_DE_LINEA)
    assert "(5.0%)" in t


def test_una_factura_sin_descuentos_no_muestra_la_fila():
    t = texto(dict(CABECERA, subtotal=3000000, total_descuentos=0,
                   total_impuestos=570000, total=3570000), [linea()])
    assert "Dto." not in t


def test_el_concepto_del_descuento_de_linea_sigue_bajo_el_producto():
    """Lo muestra la tabla de líneas, que es su sitio."""
    t = texto(dict(CABECERA, subtotal=2700000, total_descuentos=300000,
                   total_impuestos=513000, total=3213000),
              CON_DESCUENTO_DE_LINEA)
    assert "Convenio empresarial" in t
