"""
E4 — Cierre. Conclusiones, referencias bibliográficas y anexos.

Las referencias **se construyen desde `FUENTES`**, el mismo diccionario del que
salen las citas del capítulo 2. Escribir la lista aparte lleva siempre al mismo
defecto, que es una fuente citada en el cuerpo y ausente de la lista, o una lista
con fuentes que nadie citó. Aquí el generador comprueba las dos cosas y se detiene
si alguna falla.
"""
import re
from pathlib import Path

from e4_cap2 import FUENTES

GENERADOR = Path(__file__).resolve().parent

ANEXOS = [
    ("Anexo A", "Especificación de requisitos funcionales y no funcionales",
     "Catálogo completo de los 82 requisitos funcionales agrupados en ocho módulos y de los "
     "32 requisitos no funcionales, con su priorización por valor de negocio y urgencia y la "
     "matriz de trazabilidad frente a los objetivos del proyecto.",
     "FactuGest - Requisitos Funcionales y No Funcionales"),
    ("Anexo B", "Diagramas de casos de uso",
     "Los nueve diagramas de casos de uso del sistema, uno general y ocho por módulo, con la "
     "descripción de cada caso, los requisitos que cubre y la matriz de participación de los "
     "actores.",
     "FactuGest - Diagramas de Casos de Uso"),
    ("Anexo C", "Documentación de casos de uso",
     "Fichas completas de los 17 casos de uso críticos, con precondiciones, secuencia normal, "
     "flujos alternos, postcondiciones y excepciones, y los 39 casos restantes en formato "
     "breve con su precondición y su resultado esperado.",
     "FactuGest - Documentacion de Casos de Uso"),
    ("Anexo D", "Contrato de la interfaz de integración",
     "Especificación OpenAPI de las nueve operaciones de la API, generada automáticamente por "
     "el sistema y disponible en la ruta /openapi.json, con su interfaz de exploración en "
     "/docs.",
     None),
]


def escribir(d):
    _conclusiones(d)
    _referencias(d)
    _anexos(d)


def _conclusiones(d):
    d.titulo("CONCLUSIONES", nivel=1, nueva_pagina=True)
    d.parrafo(
        "El proyecto desarrolló FactuGest, una plataforma web de facturación electrónica que "
        "opera como proveedor tecnológico y permite a micro, pequeñas y medianas empresas "
        "cumplir con la obligación de facturar ante la administración tributaria sin "
        "reemplazar el software con el que ya trabajan. Los cinco objetivos específicos "
        "planteados se cumplieron, con la única salvedad de la transmisión en los servicios "
        "de producción, que depende de un trámite de habilitación ajeno al desarrollo."
    )
    d.parrafo(
        "La primera conclusión se refiere al problema y no a la solución. La elicitación "
        "mostró que la dificultad para adoptar la facturación electrónica no es "
        "principalmente económica ni de desconocimiento, sino de reemplazo, porque estas "
        "empresas ya operan con un software que concentra su catálogo, sus precios y la forma "
        "en que su personal aprendió a trabajar. Distinguir el rechazo a la obligación del "
        "rechazo al cambio de herramienta fue lo que orientó todo el desarrollo posterior, y "
        "una investigación que no hubiera hecho esa distinción habría producido un sistema de "
        "facturación más, sin resolver la barrera."
    )
    d.parrafo(
        "La segunda conclusión es que el modelo de integración por interfaz resuelve esa "
        "barrera de manera verificable. La demostración se hizo conectando un punto de venta "
        "en operación que no emitía facturación electrónica, el cual quedó expidiendo "
        "documentos válidos sin que se modificara la forma en que registra sus ventas. Ese "
        "resultado es el que convierte la propuesta en una solución y no en una intención."
    )
    d.parrafo(
        "La tercera conclusión es de orden técnico. Concentrar la lógica de negocio en una "
        "capa de servicios compartida por la aplicación web y por la interfaz de integración "
        "evitó que existieran dos implementaciones del cálculo tributario, con el riesgo de "
        "que la misma operación arrojara resultados distintos según por dónde entrara. Las "
        "190 pruebas automatizadas que respaldan esa capa cubren un solo camino y valen para "
        "las dos entradas."
    )
    d.parrafo(
        "La cuarta conclusión se refiere a las condiciones que impone un sistema con efectos "
        "tributarios. Un consecutivo repetido, un documento incompleto o un membrete "
        "equivocado no producen un defecto que el usuario pueda ignorar, sino un documento "
        "rechazado. De ahí que decisiones que en otro sistema serían optimizaciones, como "
        "reservar "
        "el número en una sola sentencia, emitir dentro de una transacción, calcular el "
        "consumo sobre los documentos reales, sean aquí condiciones de validez."
    )
    d.parrafo(
        "La quinta conclusión corresponde a la metodología. El alcance del proyecto cambió "
        "durante el desarrollo, cuando se comprobó que la barrera era el reemplazo del "
        "software, y ese cambio se incorporó reordenando el product backlog sin desechar lo "
        "construido. Un enfoque secuencial habría obligado a rehacer el análisis completo, de "
        "modo que la elección de un marco de trabajo iterativo no fue una preferencia de "
        "estilo sino una decisión que el proyecto terminó necesitando."
    )
    d.parrafo(
        "Por último, el trabajo deja líneas de continuación identificadas. La transmisión en "
        "producción ante la administración tributaria queda a la espera de la habilitación "
        "del proveedor, para lo cual el sistema ya aísla esa comunicación detrás de una capa "
        "propia. El recaudo de las mensualidades podría integrarse con pasarelas de pago, hoy "
        "registrado de forma manual. Y la interfaz de integración, construida para ser "
        "consumida por cualquier sistema, admite un cliente móvil que quedó fuera del alcance "
        "de esta versión."
    )


def _referencias(d):
    d.titulo("REFERENCIAS BIBLIOGRÁFICAS", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Las referencias se presentan en orden alfabético, según el estilo APA en su séptima "
        "edición.", sangria=False
    )
    d.parrafo()
    for _, referencia in sorted(FUENTES.values(), key=lambda f: f[1].lower()):
        # Sangría francesa: la primera línea al margen y las siguientes desplazadas,
        # que es como APA presenta cada entrada de la lista.
        p = d.parrafo(referencia, sangria=False)
        p.paragraph_format.left_indent = SANGRIA_FRANCESA
        p.paragraph_format.first_line_indent = -SANGRIA_FRANCESA


def _anexos(d):
    d.titulo("ANEXOS", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Se relacionan los documentos que acompañan a este trabajo y que contienen el detalle "
        "de los artefactos de análisis y diseño. Al cuerpo del documento se llevó una "
        "selección de cada uno, y aquí consta la referencia al material completo."
    )
    d.tabla(
        "Anexos del documento",
        ["Anexo", "Documento", "Contenido"],
        [[codigo, titulo, contenido] for codigo, titulo, contenido, _ in ANEXOS],
        nota="Elaboración propia. Los anexos A, B y C se entregan como documentos "
             "independientes; el anexo D lo genera el propio sistema.",
        anchos=[1.9, 4.6, 9.8],
    )
    d.parrafo(
        "El anexo D merece una precisión. No se trata de un documento escrito por el equipo "
        "sino de una especificación que el sistema produce a partir de su propio código, de "
        "manera que no puede desviarse de lo que la interfaz realmente hace. Esa es la razón "
        "por la cual se referencia en lugar de transcribirse, ya que una copia impresa sería "
        "válida únicamente hasta el siguiente cambio."
    )


SANGRIA_FRANCESA = None    # se resuelve al importar, con el valor del motor de formato


def _preparar():
    from apa import SANGRIA
    global SANGRIA_FRANCESA
    SANGRIA_FRANCESA = SANGRIA


def _comprobar_citas():
    """Ninguna fuente puede quedar sin citar, ni citarse una que no esté declarada."""
    texto = "".join(ruta.read_text(encoding="utf-8")
                    for ruta in GENERADOR.glob("e4_*.py"))
    citadas = set(re.findall(r"cita\('([a-z0-9]+)'\)", texto))
    declaradas = set(FUENTES)
    sin_citar = declaradas - citadas
    sin_declarar = citadas - declaradas
    if sin_citar or sin_declarar:
        raise SystemExit(
            f"Referencias sin citar en el texto: {sorted(sin_citar)} · "
            f"Citas sin referencia declarada: {sorted(sin_declarar)}")
    return len(declaradas)


_preparar()
_comprobar_citas()
