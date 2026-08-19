"""El membrete del PDF es el del emisor del documento, no el nuestro.

Esta prueba existe por un defecto que estuvo ahí sin que nadie lo viera: los
documentos emitidos por la API salían con el nombre y el logo de FactuGest,
porque `generate_invoice_pdf` no recibía el emisor y caía en sus valores por
defecto. Una factura que dice quién la expidió, diciendo a la empresa equivocada,
es el peor defecto posible en un sistema de facturación electrónica.

No toca base de datos: arma los diccionarios a mano, que es justamente el contrato
que documenta `services/documento_canonico.py`.
"""
import io

import pytest

from services.pdf_service import generate_invoice_pdf

pypdf = pytest.importorskip("pypdf", reason="pypdf solo se usa para leer el PDF de vuelta")


CLINICA = {
    "nombre": "Clinica Odontologica Sonrisas",
    "nit": "901447903", "dv": "0",
    "direccion": "Av. 0 # 14-22, consultorio 301",
    "ciudad": "San Jose De Cucuta",
    "telefono": "6075747711",
    "correo": "citas@sonrisascucuta.co",
    "regimen_tributario": "RESPONSABLE_IVA",
    "actividad_economica": "8622",
    "prefijo_factura": "COS",
    "resolucion_dian": "18764003813699",
    "resolucion_fecha_desde": "2026-01-01", "resolucion_fecha_hasta": "2026-12-31",
    "resolucion_desde": 1, "resolucion_hasta": 20000,
    "tarifa_ica": 0, "autoretenedor": 0, "gran_contribuyente": 0,
    "website": "", "logo": None,
}

DOCUMENTO = {
    "numero_factura": "COS1", "tipo_factura": "FV", "fecha": "2026-08-01 10:00:00",
    "subtotal": 180000, "total_descuentos": 0, "total_impuestos": 0, "total": 180000,
    "cufe": "a" * 96, "forma_pago": "CONTADO", "metodo_pago_nombre": "Efectivo",
    "cliente_nombre": "Rosa Elvira Parra", "document_type": "13",
    "document_number": "1090123456",
}

LINEAS = [{
    "producto_nombre": "Resina en diente", "sku": "RES-01", "unidad_medida": "94",
    "cantidad": 1, "precio_unitario": 180000, "subtotal": 180000,
    "descuento_porcentaje": 0, "descuento_valor": 0, "impuesto_porcentaje": 0,
    "impuesto_valor": 0,
}]


def texto_del_pdf(contenido: bytes) -> str:
    lector = pypdf.PdfReader(io.BytesIO(contenido))
    return " ".join(" ".join((p.extract_text() or "").split()) for p in lector.pages)


def test_el_membrete_es_del_emisor_que_se_le_pasa():
    texto = texto_del_pdf(generate_invoice_pdf(DOCUMENTO, LINEAS, emisor=CLINICA))

    assert "Clinica Odontologica Sonrisas" in texto
    assert "901447903-0" in texto
    assert "18764003813699" in texto
    assert "Av. 0 # 14-22" in texto


def test_el_membrete_nunca_cae_en_el_nuestro():
    """El defecto original, en una línea: sin emisor explícito el PDF ponía
    «Factugest». Aunque no se pase emisor, el nombre del proveedor no puede
    aparecer en la factura de un tercero."""
    texto = texto_del_pdf(generate_invoice_pdf(DOCUMENTO, LINEAS, emisor=CLINICA))
    assert "actugest" not in texto


def test_sin_emisor_explicito_lo_lee_del_documento():
    """Es como lo llama el formulario web, con los alias que trae la consulta."""
    documento = dict(DOCUMENTO, empresa_nombre="Ferreteria Los Andes S.A.S.",
                     empresa_nit="901102337", empresa_dv="9",
                     empresa_resolucion_dian="18764003812644",
                     empresa_resolucion_fecha_desde="2026-01-01",
                     empresa_resolucion_fecha_hasta="2026-12-31")
    texto = texto_del_pdf(generate_invoice_pdf(documento, LINEAS))

    assert "Ferreteria Los Andes" in texto
    assert "901102337-9" in texto


def test_sin_logo_el_membrete_imprime_el_nombre_una_sola_vez():
    """La casilla del logo queda vacía en vez de repetir el nombre para llenarla."""
    texto = texto_del_pdf(generate_invoice_pdf(DOCUMENTO, LINEAS, emisor=CLINICA))
    assert texto.count("Clinica Odontologica Sonrisas") == 1


def test_un_logo_que_no_existe_no_tumba_la_factura():
    """Si el archivo se borró del disco, la factura sale igual con el nombre."""
    emisor = dict(CLINICA, logo="no-existe.png")
    texto = texto_del_pdf(generate_invoice_pdf(DOCUMENTO, LINEAS, emisor=emisor))
    assert "Clinica Odontologica Sonrisas" in texto


def test_un_logo_con_ruta_de_escape_se_ignora():
    """El nombre lo genera el servidor, pero se comprueba igual: un «../» dentro
    convertiría el membrete en una forma de leer archivos del disco."""
    emisor = dict(CLINICA, logo="../../../main.py")
    texto = texto_del_pdf(generate_invoice_pdf(DOCUMENTO, LINEAS, emisor=emisor))
    assert "Clinica Odontologica Sonrisas" in texto


# ── Color de marca ──────────────────────────────────────────────────────────

def test_cada_emisor_pinta_con_su_color():
    """Dos emisores con colores distintos no pueden producir el mismo PDF.

    Los encabezados de tabla y los remates salían siempre en el azul de FactuGest,
    así que la factura de una comercializadora de marca roja llegaba pintada con
    la identidad de otro.
    """
    rojo = generate_invoice_pdf(DOCUMENTO, LINEAS,
                                emisor=dict(CLINICA, color_marca="#7a0000"))
    azul = generate_invoice_pdf(DOCUMENTO, LINEAS,
                                emisor=dict(CLINICA, color_marca="#4e73df"))
    assert rojo != azul


def test_un_color_mal_escrito_no_tumba_la_factura():
    """Un campo de configuración con basura no puede dejar a nadie sin documento."""
    for basura in ("azul", "#zzz", "", None, "#7a00001"):
        pdf = generate_invoice_pdf(DOCUMENTO, LINEAS,
                                   emisor=dict(CLINICA, color_marca=basura))
        assert "Clinica Odontologica Sonrisas" in texto_del_pdf(pdf)


def test_sin_color_sale_el_neutro_y_no_el_de_nadie():
    from services.pdf_service import COLOR_POR_DEFECTO, _color
    assert _color(None) == _color(COLOR_POR_DEFECTO)
    assert _color("#4e73df") != _color(None)
