"""Pruebas de la generación y el formato de las llaves de API.

La autenticación completa necesita base de datos; aquí se cubre lo que no la
necesita, que es justo donde viven las propiedades criptográficas.
"""
import pytest

from services.api_key_service import (LlaveInvalidaError, PREFIJO_BASE, _hash, _partir,
                                      generar_llave)


def test_la_llave_se_parte_en_prefijo_y_secreto():
    prefijo, llave = generar_llave()
    assert llave.startswith(prefijo + ".")

    partes = _partir(llave)
    assert partes[0] == prefijo
    assert partes[1] == llave[len(prefijo) + 1:]


def test_el_prefijo_cabe_en_la_columna_y_es_reconocible():
    prefijo, _ = generar_llave()
    assert prefijo.startswith(PREFIJO_BASE)
    # api_key_prefijo es VARCHAR(20).
    assert len(prefijo) <= 20


def test_el_secreto_tiene_entropia_suficiente():
    """Es lo que justifica hashear con SHA-256 en lugar de bcrypt."""
    _, llave = generar_llave()
    secreto = _partir(llave)[1]
    assert len(secreto) >= 30


def test_dos_llaves_seguidas_no_se_parecen():
    llaves = {generar_llave()[1] for _ in range(50)}
    prefijos = {l.split(".")[0] for l in llaves}
    assert len(llaves) == 50
    assert len(prefijos) == 50


@pytest.mark.parametrize("entrada", ["", None, "sinpunto", ".solosecreto", "soloprefijo.",
                                     "   "])
def test_una_llave_mal_formada_se_rechaza_antes_de_consultar_nada(entrada):
    with pytest.raises(LlaveInvalidaError):
        _partir(entrada)


def test_el_hash_es_estable_y_no_deja_ver_el_secreto():
    _, llave = generar_llave()
    secreto = _partir(llave)[1]

    assert _hash(secreto) == _hash(secreto)
    assert _hash(secreto) != _hash(secreto + "x")
    assert secreto not in _hash(secreto)
    assert len(_hash(secreto)) == 64
