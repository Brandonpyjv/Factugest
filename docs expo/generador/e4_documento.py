"""
E4 — Documento de grado de FactuGest. Ensamblador.

Cada capítulo vive en su propio módulo y expone una función `escribir(d)` que
recibe el documento y le agrega su parte. Aquí solo se declara el orden.

**Por qué así.** El documento se escribe en sesiones distintas, una por capítulo.
Con todo en un archivo, cada sesión tendría que releer y reescribir el conjunto —y
el riesgo no es el trabajo perdido sino el capítulo que queda a medias—. Separado,
una sesión toca un archivo y el ensamble es esta lista. Los contadores de tablas y
figuras corren solos de un capítulo al siguiente porque el documento es uno solo.

    python e4_documento.py
"""
from pathlib import Path

from apa import DocumentoAPA

import e4_cap1
import e4_cap2
import e4_cap3
import e4_cap4
import e4_cap5a
import e4_cap5b
import e4_cap6a
import e4_cap6b
import e4_cierre
import e4_preliminares

SALIDA = Path(__file__).resolve().parent.parent / "entregables"
ARCHIVO = SALIDA / "FactuGest - Documento de Grado.docx"

# El orden de esta lista es el orden del documento.
CAPITULOS = [
    e4_preliminares,
    e4_cap1,
    e4_cap2,
    e4_cap3,
    e4_cap4,
    e4_cap5a,
    e4_cap5b,
    e4_cap6a,
    e4_cap6b,
    e4_cierre,
]


def construir():
    d = DocumentoAPA()
    for capitulo in CAPITULOS:
        capitulo.escribir(d)
    SALIDA.mkdir(parents=True, exist_ok=True)
    d.guardar(ARCHIVO)
    return d


if __name__ == "__main__":
    documento = construir()
    print(f"Generado: {ARCHIVO}")
    print(f"Capítulos escritos: {len(CAPITULOS)}")
    print(f"Tablas: {documento.n_tabla} · Figuras: {documento.n_figura}")
