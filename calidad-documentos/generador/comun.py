"""
Lo que comparten los dos entregables de la competencia de calidad.

El motor de formato no se copia aquí. Se reutiliza el del documento de grado
(`docs expo/generador/apa.py`), porque los dos entregables van al mismo instructivo
APA y una segunda copia del motor se desincroniza en cuanto alguien corrija un
margen en una sola de las dos.

Los datos de portada tampoco se reescriben, se importan de `e4_preliminares`, que es
donde ya estaban. Si un integrante cambia de nombre, cambia en un solo sitio.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
GENERADOR_GRADO = RAIZ / "docs expo" / "generador"
SALIDA = Path(__file__).resolve().parent.parent / "entregables"

if str(GENERADOR_GRADO) not in sys.path:
    sys.path.insert(0, str(GENERADOR_GRADO))

from apa import DocumentoAPA                                    # noqa: E402
from e4_preliminares import (INTEGRANTES, FICHA, PROGRAMA,      # noqa: E402
                             CENTRO, CIUDAD, ANIO)

COMPETENCIA = "Controlar la calidad del servicio de software de acuerdo con los estándares técnicos"
GUIA = "GFPI-F-135"
INSTRUCTORA = "HEIDY LIZBETH ADARME"

INSTITUCION = ["SERVICIO NACIONAL DE APRENDIZAJE (SENA)", CENTRO, PROGRAMA]


def nuevo_documento(titulo, subtitulo, evidencia):
    """Devuelve un documento con la portada de la evidencia ya escrita.

    La portada nombra la evidencia y la competencia porque estos dos archivos se
    entregan sueltos en la plataforma, sin el documento de grado alrededor que
    diga de qué guía salieron.
    """
    d = DocumentoAPA()
    d.portada(
        titulo=titulo,
        subtitulo=subtitulo,
        integrantes=INTEGRANTES,
        grado=f"Ficha {FICHA}\n{PROGRAMA}\n\n{evidencia}\n{COMPETENCIA}\n\n"
              f"Instructora: {INSTRUCTORA}",
        institucion=INSTITUCION,
        ciudad=CIUDAD,
        anio=ANIO,
    )
    return d


def guardar(d, nombre):
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = SALIDA / nombre
    d.guardar(ruta)
    return ruta
