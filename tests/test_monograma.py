"""El distintivo de una empresa que no cargó logo.

Lo que se fija aquí es que el mismo nombre dé siempre el mismo par de iniciales y
el mismo color. Un distintivo que cambia entre una factura y la siguiente —o entre
el panel y el PDF— no distingue nada; y las iniciales salen impresas en un
documento fiscal, así que no pueden depender del orden de un `set` ni del azar.
"""
import io

import pytest

from services.monograma import color, iniciales


@pytest.mark.parametrize("nombre, esperado", [
    ("Drogueria La Salud S.A.S.", "DS"),      # se salta el artículo
    ("Transportes del Norte S.A.S.", "TN"),   # se salta la preposición
    ("Hotel Casa Blanca", "HC"),
    ("Ferreteria Los Andes Ltda", "FA"),      # se salta la forma jurídica
    ("Droguería La Salud", "DS"),             # las tildes no cambian la inicial
])
def test_toma_las_dos_primeras_palabras_con_significado(nombre, esperado):
    assert iniciales(nombre) == esperado


def test_un_nombre_de_una_sola_palabra_usa_sus_dos_mayusculas():
    """«FactuGest S.A.S.» debe dar FG. Al partir los puntos, «S.A.S.» se convierte
    en tres palabras de una letra; si se colaran, daría «FS»."""
    assert iniciales("FactuGest S.A.S.") == "FG"
    assert iniciales("Siste Soluciones S.A.S.") == "SS"


def test_un_nombre_sin_mayusculas_usa_sus_dos_primeras_letras():
    assert iniciales("panaderia") == "PA"


def test_un_nombre_vacio_no_revienta():
    """Va dentro de la generación de un PDF: nunca puede tumbar la factura."""
    assert iniciales("") == "?"
    assert iniciales(None) == "?"
    assert iniciales("S.A.S.") == "?"


def test_el_color_de_la_empresa_manda_sobre_el_derivado():
    assert color("Siste Soluciones S.A.S.", "#c1272d") == "#c1272d"


def test_sin_color_propio_el_derivado_es_siempre_el_mismo():
    """Es la razón de no usar `random`: el distintivo tiene que ser reconocible."""
    assert color("Hotel Casa Blanca") == color("Hotel Casa Blanca")
    assert color("Hotel Casa Blanca", "") == color("Hotel Casa Blanca", None)


def test_un_color_mal_escrito_no_se_cuela_en_el_documento():
    """Un valor inválido pintaría de negro o reventaría ReportLab."""
    for malo in ("azul", "#zzz", "334155", "#33415"):
        assert color("Hotel Casa Blanca", malo) == color("Hotel Casa Blanca")


def test_dos_empresas_distintas_no_tienen_que_verse_iguales():
    nombres = ["Hotel Casa Blanca", "Drogueria La Salud", "Transportes del Norte",
               "Panaderia Trigo de Oro", "Papeleria Escolar"]
    distintivos = {(iniciales(n), color(n)) for n in nombres}
    assert len(distintivos) == len(nombres)


def test_el_pdf_dibuja_el_monograma_cuando_no_hay_logo():
    """Sin esto, la casilla del logo quedaba vacía."""
    pypdf = pytest.importorskip("pypdf")
    from services.pdf_service import generate_invoice_pdf
    from tests.test_pdf_descuentos import CABECERA, EMISOR, linea

    pdf = generate_invoice_pdf(
        dict(CABECERA, subtotal=3000000, total_descuentos=0,
             total_impuestos=570000, total=3570000),
        [linea()],
        emisor=dict(EMISOR, nombre="Hotel Casa Blanca", logo=None),
    )
    texto = " ".join((p.extract_text() or "") for p in pypdf.PdfReader(io.BytesIO(pdf)).pages)
    assert "HC" in texto
