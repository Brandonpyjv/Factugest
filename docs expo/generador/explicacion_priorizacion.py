"""
Cómo se obtienen las cifras de las diapositivas 16 a 19 de la sustentación.

Documento de apoyo para la defensa, no un entregable del documento de grado. Existe
porque en esas cuatro diapositivas aparecen números —el puntaje de un requisito, el
promedio de un módulo, el conteo de críticos— y quien sustenta tiene que poder
explicar de dónde sale cada uno sin abrir el código delante del jurado.

**Ninguna cifra está escrita aquí a mano.** Los ejemplos, las bandas y los promedios
se calculan importando `e1_requisitos.py`, que es el mismo módulo del que se
alimentan el capítulo 4 del documento y las diapositivas. Si mañana cambia la
calificación de un requisito, este documento cambia con ella; escrito a mano, sería
la tercera versión de la misma cifra.

    python explicacion_priorizacion.py
"""
from pathlib import Path

from apa import DocumentoAPA
from diagramas_proceso import CUADRANTES
from e1_requisitos import MODULOS, RNF, prioridad, puntaje

SALIDA = Path(__file__).resolve().parent.parent / "entregables"
ARCHIVO = SALIDA / "FactuGest - Cálculo de las diapositivas 16 a 19.docx"


def _coma(numero):
    """En español el separador decimal es la coma, y el documento se lee en español."""
    return f"{numero}".replace(".", ",")


def _buscar(codigo):
    for _, nombre_modulo, _, _, reqs in MODULOS:
        for requisito in reqs:
            if requisito[0] == codigo:
                return nombre_modulo, requisito
    raise KeyError(codigo)


def _fila_ejemplo(codigo):
    _, (_, nombre, _, _, valor, urgencia) = _buscar(codigo)
    return [f"{codigo} {nombre}", str(valor), str(urgencia),
            f"{valor} x 0,6 + {urgencia} x 0,4", _coma(puntaje(valor, urgencia)),
            prioridad(valor, urgencia)]


def _promedio(reqs):
    return round(sum(puntaje(v, u) for *_, v, u in reqs) / len(reqs), 1)


def _criticos(reqs):
    return sum(1 for *_, v, u in reqs if prioridad(v, u) == "Crítica")


def _trazabilidad(doc):
    doc.titulo("Diapositivas 16 y 17. Aquí no se calcula, se traza", nivel=2)
    doc.parrafo(
        "En estas dos no hay ninguna operación aritmética. Lo que hay es una regla de "
        "trazabilidad que el proyecto sostiene de principio a fin: cada técnica de "
        "captura tiene que producir historias de usuario, y cada historia tiene que "
        "producir requisitos funcionales. Por eso las diapositivas van de a tres.")
    doc.tabla(
        "Cadena de trazabilidad de las dos técnicas de captura",
        ["Técnica de captura", "Historias que produjo", "Requisitos que produjo"],
        [["Encuesta a 45 empresas (diapositiva 12)", "Diapositiva 13", "Diapositiva 14"],
         ["Observación directa (diapositiva 15)", "Diapositiva 16", "Diapositiva 17"]],
        nota="La diapositiva 16 muestra las historias HU-01, HU-02 y HU-11, y la 17 los "
             "requisitos RF 1.1, RF 1.2, RF 1.8 y RF 5.1 que se derivan de ellas. Si el "
             "jurado pregunta de dónde salió una historia, la respuesta está en la "
             "diapositiva anterior.",
        anchos=[5.5, 5.5, 5.5])
    doc.parrafo(
        "El código de un requisito tampoco es arbitrario y conviene poder leerlo en voz "
        "alta: en RF 1.8, el 1 es el módulo de gestión de clientes API y el 8 es el "
        "octavo requisito de ese módulo. Los ocho módulos y sus requisitos son los "
        "mismos del capítulo 4 del documento de grado.")


def _stakeholders(doc):
    doc.titulo("Diapositiva 18. La matriz de interesados no es un puntaje", nivel=2)
    doc.parrafo(
        "La matriz no pondera nada: clasifica. A cada interesado se le hacen dos "
        "preguntas de sí o no, y el cruce de las dos respuestas lo deja en uno de los "
        "cuatro cuadrantes. La primera es si puede cambiar el rumbo del proyecto, que "
        "es su influencia; la segunda es si le afecta directamente el resultado, que es "
        "su interés. El cuadrante no describe al interesado, indica qué hacer con él.")
    doc.tabla(
        "Cuadrantes de la matriz de influencia e interés",
        ["Cuadrante", "Criterio", "Interesados"],
        [[rotulo, criterio.replace("· Baja", "y baja").replace("· Alta", "y alta"),
          "; ".join(nombre.replace("\n", " ") for nombre in gente)]
         for rotulo, criterio, _, gente in CUADRANTES.values()],
        nota="La DIAN queda en alta influencia y bajo interés porque no participa del "
             "proyecto, pero fija las condiciones que todo documento debe cumplir. Su "
             "cuadrante indica la estrategia: mantenerla informada sin esperar que "
             "intervenga.",
        anchos=[3.2, 5.3, 8.0])


def _priorizacion(doc):
    doc.titulo("Diapositiva 19. Aquí sí hay una fórmula", nivel=2)
    doc.parrafo(
        "Cada requisito se califica con dos números de uno a cinco, su valor de negocio "
        "y su urgencia, y los dos se combinan ponderados en un solo puntaje:")
    doc.parrafo("puntaje = (valor de negocio x 0,6) + (urgencia x 0,4)",
                sangria=False, negrita=True)
    doc.parrafo(
        "El reparto de sesenta y cuarenta no es arbitrario. Lo importante debe pesar "
        "más que lo afanado, porque un requisito urgente pero de bajo valor desplazaría "
        "recursos de otro que sostiene la operación. Esa ponderación es la única "
        "diferencia entre esta técnica y ordenar los requisitos por la fecha en que "
        "alguien los pidió.")
    doc.tabla(
        "Escala de calificación de los dos criterios",
        ["Puntaje", "Valor de negocio", "Urgencia"],
        [["1", "Impacto muy bajo para la operación", "No es urgente, puede esperar"],
         ["2", "Impacto bajo, aporta poca funcionalidad", "Poco urgente"],
         ["3", "Impacto medio, mejora procesos importantes", "Urgencia moderada"],
         ["4", "Impacto alto, necesario para operar", "Muy urgente"],
         ["5", "Impacto crítico, indispensable", "Debe implementarse de inmediato"]],
        nota="Es la tabla que se proyecta en la diapositiva 19.",
        anchos=[2.2, 7.3, 7.0])
    doc.parrafo(
        "El puntaje resultante cae después en una de cuatro bandas, y esa banda es la "
        "que aparece en la columna «Prioridad» del catálogo de requisitos.")
    doc.tabla(
        "Bandas de prioridad",
        ["Puntaje obtenido", "Prioridad"],
        [["4,6 o más", "Crítica"],
         ["Entre 4,0 y 4,5", "Alta"],
         ["Entre 3,0 y 3,9", "Media"],
         ["Menos de 3,0", "Baja"]],
        nota="Los cortes están puestos donde la combinación de calificaciones cambia de "
             "significado: un requisito solo llega a crítica si obtuvo cinco y cuatro, o "
             "cinco y cinco, en los dos criterios.",
        anchos=[6.0, 4.0])
    doc.parrafo(
        "Cuatro ejemplos tomados del propio catálogo, que es de donde se calculan las "
        "tablas de la sustentación:")
    doc.tabla(
        "Ejemplos del cálculo del puntaje",
        ["Requisito", "Valor", "Urgencia", "Operación", "Puntaje", "Prioridad"],
        [_fila_ejemplo(codigo) for codigo in ("RF 1.1", "RF 1.7", "RF 1.4", "RF 1.9")],
        nota="El primero obtuvo la calificación máxima en los dos criterios y el último "
             "quedó en baja, porque eliminar un cliente integrado ni aporta a la "
             "operación ni corre prisa.",
        anchos=[4.6, 1.5, 1.9, 3.4, 1.8, 2.3])


def _derivadas(doc):
    doc.titulo("De dónde salen las diapositivas 20 y 21", nivel=2)
    doc.parrafo(
        "Las dos se calculan a partir del puntaje de cada requisito, y por eso vienen "
        "inmediatamente después. El puntaje de un módulo es el promedio de los puntajes "
        "de los requisitos que contiene, y la columna de críticos es el conteo de los "
        "que quedaron en la banda más alta.")
    total = sum(len(reqs) for *_, reqs in MODULOS)
    criticos = sum(_criticos(reqs) for *_, reqs in MODULOS)
    general = round(
        sum(puntaje(v, u) for *_, reqs in MODULOS for *_, v, u in reqs) / total, 1)
    filas = [[codigo, nombre, str(len(reqs)), _coma(_promedio(reqs)), str(_criticos(reqs))]
             for codigo, nombre, _, _, reqs in MODULOS]
    doc.tabla(
        "Puntaje promedio y requisitos críticos por módulo",
        ["Código", "Módulo", "Requisitos", "Promedio", "Críticos"],
        filas + [["", "Total", str(total), _coma(general), str(criticos)]],
        nota=f"Encabeza la lista el módulo de documentos electrónicos, del que depende "
             f"que un documento salga correctamente expedido, y cierra el de "
             f"configuración y catálogos, que agrupa parámetros que se ajustan de vez en "
             f"cuando. El sistema quedó con {total} requisitos funcionales, de los "
             f"cuales {criticos} son críticos, y {len(RNF)} requisitos no funcionales.",
        anchos=[2.0, 7.0, 2.6, 2.4, 2.5])


def escribir():
    doc = DocumentoAPA()
    doc.titulo("Cómo se obtienen las cifras de las diapositivas 16 a 19", nivel=1)
    doc.parrafo(
        "Las cuatro diapositivas forman una sola cadena y conviene explicarlas en ese "
        "orden, porque cada una toma lo que dejó la anterior. Las dos primeras no "
        "calculan nada: trazan de dónde viene cada requisito. Las dos últimas sí "
        "calculan, y de ellas salen además los números de las diapositivas 20 y 21.")

    _trazabilidad(doc)
    _stakeholders(doc)
    _priorizacion(doc)
    _derivadas(doc)

    doc.titulo("Dónde vive el cálculo", nivel=2)
    doc.parrafo(
        "La fórmula, las bandas y la calificación de cada requisito están en el módulo "
        "e1_requisitos.py del generador, en las funciones puntaje y prioridad. De ahí "
        "las leen el capítulo 4 del documento de grado, las tablas de la sustentación y "
        "este documento, de modo que los tres no puedan decir cifras distintas. Los "
        "cuadrantes de la matriz de interesados están en diagramas_proceso.py, en la "
        "constante CUADRANTES, que es la que dibuja la figura de la diapositiva 18.")

    SALIDA.mkdir(parents=True, exist_ok=True)
    return doc.guardar(ARCHIVO)


if __name__ == "__main__":
    print("Generado:", escribir())
