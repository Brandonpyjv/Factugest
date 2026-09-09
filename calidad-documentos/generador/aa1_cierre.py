"""
AA1, cierre. Referencias y anexos.

Las referencias se construyen desde las claves que cada capítulo declaró en su
`CITADAS`, no de una lista escrita aparte, y el archivo comprueba que no quede una
fuente citada sin referencia ni una referencia que nadie citó. Es el error más
frecuente de una bibliografía hecha a mano y el más fácil de evitar por código.

El anexo con las pruebas también se genera, leyendo la salida de la corrida que se
guardó en `evidencia/`. Escribir a mano una lista de ciento noventa nombres sería
copiar durante media hora algo que ya está escrito, y bastaría con que alguien
agregara una prueba para que el anexo dejara de corresponder con la realidad.
"""
import re

from apa import SANGRIA
from comun import RAIZ
from evidencia import DURACION, FECHA_CORRIDA, HERRAMIENTA, TOTAL_UNITARIAS, UNITARIAS
from fuentes import FUENTES, usadas

import aa1_cap1_marco
import aa1_cap2_adopcion
import aa1_cap3_plan
import aa1_cap4_ejecutadas
import aa1_cap5_planificadas

CITADAS = []

SALIDA_PYTEST = RAIZ / "calidad-documentos" / "evidencia" / "pytest_salida.txt"

CAPITULOS = [aa1_cap1_marco, aa1_cap2_adopcion, aa1_cap3_plan, aa1_cap4_ejecutadas,
             aa1_cap5_planificadas]


def _citadas_del_informe():
    claves = set()
    for capitulo in CAPITULOS:
        claves.update(capitulo.CITADAS)
    return claves


def _pruebas_de_la_corrida():
    """Las pruebas superadas, leídas de la salida guardada de la corrida.

    Devuelve pares de archivo y nombre, en el orden en que se ejecutaron. El nombre
    se deja tal como lo escribió quien programó la prueba, porque está redactado
    para leerse y decir qué comprueba.
    """
    # El identificador puede llevar espacios cuando una prueba se ejecuta con varios
    # juegos de datos y alguno es una frase, así que se corta por la palabra PASSED
    # y no por el primer espacio.
    patron = re.compile(r"^tests[\\/](\S+\.py)::(.+?)\s+PASSED")
    pruebas = []
    for linea in SALIDA_PYTEST.read_text(encoding="utf-8", errors="ignore").splitlines():
        encontrado = patron.match(linea)
        if encontrado:
            pruebas.append((encontrado.group(1), encontrado.group(2)))
    return pruebas


def _legible(nombre):
    """De «test_el_membrete_es_del_emisor» a «El membrete es del emisor»."""
    caso, _, datos = nombre.partition("[")
    texto = caso.removeprefix("test_").replace("_", " ").strip()
    texto = texto[:1].upper() + texto[1:]
    return f"{texto} [{datos}" if datos else texto


def escribir(d):
    _referencias(d)
    _anexos(d)


def _referencias(d):
    d.titulo("9. Referencias", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Las referencias se presentan en orden alfabético, según el estilo APA en su "
        "séptima edición. Las normas se citan por el organismo que las publica y el año "
        "de la versión utilizada.",
        sangria=False,
    )
    d.parrafo()
    for referencia in usadas(_citadas_del_informe()):
        p = d.parrafo(referencia, sangria=False)
        p.paragraph_format.left_indent = SANGRIA
        p.paragraph_format.first_line_indent = -SANGRIA


def _anexos(d):
    pruebas = _pruebas_de_la_corrida()

    d.titulo("10. Anexos", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Se relacionan las evidencias que respaldan lo afirmado en el informe. Las tres "
        "primeras se producen solas al ejecutar el sistema o su batería de pruebas, de "
        "modo que cualquiera puede reproducirlas."
    )
    d.tabla(
        "Anexos del informe",
        ["Anexo", "Contenido", "Dónde está"],
        [["A", "Salida de la corrida de la batería de pruebas",
          "Se transcribe a continuación y se conserva en el repositorio del proyecto"],
         ["B", f"Listado de las {TOTAL_UNITARIAS} pruebas superadas, con su nombre",
          "Se transcribe a continuación, obtenido de la misma corrida"],
         ["C", "Colección de peticiones de prueba de la interfaz de integración",
          "En el repositorio del proyecto, en formato de intercambio de la herramienta"],
         ["D", "Imágenes de las pruebas funcionales",
          "En el repositorio del proyecto, ocho imágenes de cuatro operaciones"],
         ["E", "Catálogo de requisitos funcionales y no funcionales",
          "Entregable independiente del proyecto, del que salen los requisitos "
          "clasificados en el capítulo 3"]],
        nota="Los anexos A y B se generan al ejecutar la batería y no se escriben a mano, "
             "de manera que corresponden siempre a la última corrida.",
        anchos=[1.4, 6.0, 7.4],
    )

    d.titulo("Anexo A. Salida de la corrida de pruebas", nivel=2, nueva_pagina=True)
    d.parrafo(
        f"Corrida del {FECHA_CORRIDA} con {HERRAMIENTA}. La batería completa terminó en "
        f"{DURACION} sin ninguna falla."
    )
    d.tabla(
        "Resultado de la corrida por archivo de pruebas",
        ["Archivo", "Pruebas", "Resultado"],
        ([[archivo, str(cantidad), "Todas superadas"]
          for archivo, cantidad, _ in UNITARIAS]
         + [["Total", str(TOTAL_UNITARIAS), "Sin fallas"]]),
        nota="La última fila es el resultado de la sesión completa, tal como lo reporta "
             "la herramienta al terminar.",
        anchos=[6.4, 2.2, 6.2],
    )

    d.titulo("Anexo B. Listado de las pruebas superadas", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El nombre de cada prueba se deja tal como está escrito en el código, porque está "
        "redactado para decir qué comprueba y no para nombrar una función. Leído de "
        "corrido, este listado es la descripción más precisa de lo que el sistema "
        "garantiza. Entre corchetes aparecen los datos con los que se ejecutó una prueba "
        "escrita una vez y corrida con varios juegos de valores."
    )
    ancho = d.seccion_horizontal()
    d.tabla(
        f"Las {len(pruebas)} pruebas superadas en la corrida",
        ["N.º", "Archivo", "Prueba"],
        [[str(numero), archivo, _legible(nombre)]
         for numero, (archivo, nombre) in enumerate(pruebas, 1)],
        nota="Listado obtenido de la salida de la corrida, sin edición manual.",
        anchos=[1.2, 5.6, 15.4],
    )
    # No se vuelve a vertical porque este anexo cierra el informe, y abrir una sección
    # nueva para nada deja una última hoja en blanco.


def _comprobar():
    """Que la bibliografía y las citas del texto digan lo mismo."""
    citadas = _citadas_del_informe()
    sin_declarar = citadas - set(FUENTES)
    assert not sin_declarar, f"Citas sin referencia declarada: {sorted(sin_declarar)}"
    sin_citar = set(FUENTES) - citadas
    assert not sin_citar, f"Referencias que nadie citó: {sorted(sin_citar)}"
    assert SALIDA_PYTEST.exists(), f"Falta la salida de la corrida en {SALIDA_PYTEST}"
    assert len(_pruebas_de_la_corrida()) == TOTAL_UNITARIAS, (
        "La corrida guardada no tiene el número de pruebas que declara el informe")


_comprobar()
