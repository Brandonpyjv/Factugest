"""
Pruebas del contrato de la API.

Interesa sobre todo comprobar que las reglas son las mismas que las del
formulario web: si alguien cambia `validaciones.py`, la API tiene que cambiar
con él. Por eso varias pruebas comparan contra el mensaje del dominio en lugar
de repetirlo aquí.
"""
import pytest
from pydantic import ValidationError

from routes.api.v1.modelos import (DescuentoGlobal, FacturaRequest, Impuesto, Item,
                                   Receptor)

RECEPTOR = {
    "tipo_documento": "13",
    "numero_documento": "1090234567",
    "nombre": "María Fernanda Ospina",
}

ITEM = {
    "descripcion": "Teclado mecánico Redragon K552",
    "cantidad": 2,
    "precio_unitario": 189000,
    "impuesto": {"codigo": "01", "porcentaje": 19},
}


def factura(**cambios):
    base = {"receptor": dict(RECEPTOR), "items": [dict(ITEM)]}
    base.update(cambios)
    return FacturaRequest(**base)


def error(modelo, **datos) -> str:
    with pytest.raises(ValidationError) as capturado:
        modelo(**datos)
    return str(capturado.value)


# ── Camino feliz ────────────────────────────────────────────────────────────

def test_una_factura_minima_es_valida():
    f = factura()
    assert f.forma_pago == "CONTADO"
    assert f.plazo_dias == 0
    assert f.items[0].impuesto.porcentaje == 19
    assert f.enviar_email is False


def test_los_datos_se_normalizan_al_validar():
    f = factura(receptor={**RECEPTOR, "numero_documento": "1.090.234.567",
                          "email": "MOspina@Correo.com"},
                forma_pago="contado")
    assert f.receptor.numero_documento == "1090234567"
    assert f.receptor.email == "mospina@correo.com"
    assert f.forma_pago == "CONTADO"


# ── El receptor usa las reglas del dominio ──────────────────────────────────

def test_la_cedula_no_admite_letras():
    assert "solo admite números" in error(
        Receptor, **{**RECEPTOR, "numero_documento": "AB1234"})


def test_el_pasaporte_si_admite_letras():
    r = Receptor(**{**RECEPTOR, "tipo_documento": "41", "numero_documento": "AV123456"})
    assert r.numero_documento == "AV123456"


def test_el_tipo_de_documento_es_del_catalogo_dian():
    assert "no es un tipo de documento válido" in error(
        Receptor, **{**RECEPTOR, "tipo_documento": "CC"}).lower()


def test_una_persona_natural_no_lleva_numeros_en_el_nombre():
    assert "No puede contener números" in error(
        Receptor, **{**RECEPTOR, "nombre": "Juan 3ro"})


def test_una_persona_juridica_si():
    """La misma distinción que hace el formulario web."""
    r = Receptor(**{**RECEPTOR, "tipo_documento": "31",
                    "numero_documento": "9012345671",
                    "tipo_persona": "JURIDICA", "nombre": "Comercial 3M S.A.S."})
    assert r.nombre == "Comercial 3M S.A.S."


def test_el_regimen_y_el_tipo_de_persona_son_listas_cerradas():
    assert "No es una opción válida" in error(
        Receptor, **{**RECEPTOR, "tipo_persona": "ROBOT"})
    assert "No es una opción válida" in error(
        Receptor, **{**RECEPTOR, "regimen_tributario": "EXENTO_TOTAL"})


def test_el_correo_debe_tener_forma_de_correo():
    assert "No parece un correo válido" in error(
        Receptor, **{**RECEPTOR, "email": "roto@"})


# ── Las líneas ──────────────────────────────────────────────────────────────

def test_el_precio_debe_ser_mayor_que_cero():
    assert "Debe ser mayor que cero" in error(Item, **{**ITEM, "precio_unitario": 0})
    assert "No puede ser negativo" in error(Item, **{**ITEM, "precio_unitario": -1})


def test_la_cantidad_admite_decimales_pero_no_cero():
    assert Item(**{**ITEM, "cantidad": 2.5}).cantidad == 2.5
    assert error(Item, **{**ITEM, "cantidad": 0})
    assert error(Item, **{**ITEM, "cantidad": -3})


def test_el_descuento_de_linea_va_de_cero_a_cien():
    assert "No puede ser mayor que 100" in error(
        Item, **{**ITEM, "descuento_porcentaje": 150})


def test_el_codigo_de_impuesto_es_del_anexo_dian():
    assert Impuesto(codigo="zy").codigo == "ZY"
    assert "No es una opción válida" in error(Impuesto, codigo="99")


def test_el_codigo_del_item_no_se_valida_contra_nuestro_catalogo():
    """El producto es del sistema del cliente; el SKU es suyo, no nuestro."""
    assert Item(**{**ITEM, "codigo": "lo que sea 123"}).codigo == "lo que sea 123"


def test_una_factura_necesita_al_menos_una_linea():
    assert error(FacturaRequest, receptor=dict(RECEPTOR), items=[])


# ── Coherencia entre campos ─────────────────────────────────────────────────

def test_a_credito_hace_falta_plazo():
    with pytest.raises(ValidationError) as e:
        factura(forma_pago="CREDITO", plazo_dias=0)
    assert "necesita un plazo" in str(e.value)


def test_de_contado_no_lleva_plazo():
    with pytest.raises(ValidationError) as e:
        factura(forma_pago="CONTADO", plazo_dias=30)
    assert "no lleva plazo" in str(e.value)


def test_el_plazo_tiene_un_tope_razonable():
    assert factura(forma_pago="CREDITO", plazo_dias=365).plazo_dias == 365
    with pytest.raises(ValidationError):
        factura(forma_pago="CREDITO", plazo_dias=9999)


def test_el_descuento_global_no_puede_pasarse_de_la_base():
    # 2 x 189000 = 378000 de base
    assert factura(descuento_global={"valor": 100000}).descuento_global.valor == 100000
    with pytest.raises(ValidationError) as e:
        factura(descuento_global={"valor": 500000})
    assert "no puede pasar de la base" in str(e.value)


def test_el_descuento_global_no_puede_ser_negativo():
    assert "No puede ser negativo" in error(DescuentoGlobal, valor=-1)


def test_el_descuento_global_considera_los_descuentos_de_linea():
    """Con 10 % de descuento en la línea la base baja, y el tope baja con ella."""
    with pytest.raises(ValidationError):
        factura(items=[{**ITEM, "descuento_porcentaje": 10}],
                descuento_global={"valor": 350000})


# ── El ejemplo de la documentación tiene que ser válido ─────────────────────

def test_el_ejemplo_que_muestra_swagger_se_puede_enviar():
    ejemplo = FacturaRequest.model_config["json_schema_extra"]["examples"][0]
    f = FacturaRequest(**ejemplo)
    assert f.referencia_externa == "VENTA-1043"
    assert f.items[0].descuento_porcentaje == 5
