"""Pruebas del cupo: cuándo se avisa y cuándo se cobra de más.

El conteo sale de la base y no se prueba aquí. Lo que sí se prueba es la regla que
convierte ese conteo en dinero —el excedente— y en el aviso comercial, porque un
error ahí se le factura al cliente.
"""
import pytest

from services.consumo_service import _con_cupo


def fila(emitidos, cupo):
    return _con_cupo({"emitidos": emitidos, "limite_mensual": cupo})


def test_un_plan_sin_tope_nunca_genera_excedente():
    f = fila(4000, None)
    assert f["excedente"] == 0
    assert f["porcentaje"] is None
    assert f["semaforo"] == "SIN_TOPE"


def test_por_debajo_del_cupo_no_se_cobra_nada_de_mas():
    f = fila(120, 400)
    assert f["excedente"] == 0
    assert f["semaforo"] == "NORMAL"
    assert f["porcentaje"] == 30.0


def test_el_excedente_es_lo_que_pasa_del_cupo_y_no_el_total():
    f = fila(418, 400)
    assert f["excedente"] == 18


def test_justo_en_el_cupo_todavia_no_hay_excedente():
    f = fila(400, 400)
    assert f["excedente"] == 0
    assert f["semaforo"] == "ALERTA"


@pytest.mark.parametrize("emitidos, esperado", [
    (319, "NORMAL"),      # 79,75 %
    (320, "ALERTA"),      # 80 % justo: es cuando hay que ofrecer el plan siguiente
    (401, "EXCEDIDO"),
])
def test_el_semaforo_avisa_antes_de_que_le_rebote_una_emision(emitidos, esperado):
    assert fila(emitidos, 400)["semaforo"] == esperado


def test_un_cliente_que_no_emitio_nada_no_rompe_el_calculo():
    f = fila(0, 150)
    assert f["porcentaje"] == 0.0
    assert f["semaforo"] == "NORMAL"


def test_el_conteo_llega_como_decimal_desde_mysql():
    """`SUM(...)` devuelve Decimal, no int: si el cálculo no lo tolera, la tabla
    del panel revienta con datos perfectamente normales."""
    from decimal import Decimal
    f = _con_cupo({"emitidos": Decimal("418"), "limite_mensual": 400})
    assert f["excedente"] == 18
