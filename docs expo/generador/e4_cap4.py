"""
E4 — Capítulo 4. Análisis y especificación de requisitos.

**Los requisitos se importan de `e1_requisitos.py`, no se copian.** La prioridad de
cada uno se deriva de su valor de negocio y su urgencia, de modo que este capítulo
y el documento de especificación no pueden decir cosas distintas del mismo
requisito. Si se escribieran aquí a mano, bastaría cambiar un puntaje en E1 para
que los dos documentos se contradijeran, y nadie lo notaría hasta la sustentación.

Al documento de grado va la **selección de requisitos de prioridad crítica**; el
catálogo completo de 82 requisitos queda en el documento de especificación, que se
anexa.
"""
from pathlib import Path

from e1_requisitos import MODULOS, RNF, prioridad, puntaje
from e4_cap1 import OBJETIVOS_ESPECIFICOS

IMAGENES = Path(__file__).resolve().parent.parent / "entregables" / "diagramas"

HISTORIAS = [
    ("HU-01", "Como administrador, quiero registrar una empresa cliente y generar su llave de "
              "acceso para que su sistema pueda empezar a emitir documentos electrónicos."),
    ("HU-02", "Como administrador, quiero rotar la llave de un cliente para revocar una "
              "credencial comprometida sin interrumpir el servicio."),
    ("HU-03", "Como sistema cliente, quiero enviar los datos de una venta y recibir el "
              "documento ya emitido para cumplir con la obligación sin cambiar el software "
              "con el que opero."),
    ("HU-04", "Como sistema cliente, quiero reenviar una emisión con la misma referencia y "
              "obtener el documento ya expedido para poder reintentar sin duplicar facturas."),
    ("HU-05", "Como sistema cliente, quiero emitir una nota crédito referida a una factura "
              "para corregir un documento equivocado ante la administración tributaria."),
    ("HU-06", "Como comprador, quiero recibir el PDF y el XML en mi correo para contar con el "
              "soporte de la compra sin tener que solicitarlo."),
    ("HU-07", "Como administrador, quiero consultar el consumo de cada cliente contra el cupo "
              "de su plan para saber a quién ofrecerle el plan siguiente antes de que le "
              "rebote una emisión."),
    ("HU-08", "Como administrador, quiero facturar la mensualidad de un cliente por el "
              "periodo cerrado para cobrar el servicio prestado sin calcular a mano los "
              "excedentes."),
    ("HU-09", "Como cajero, quiero emitir una factura desde el panel para vender un plan a un "
              "cliente sin depender de un sistema externo."),
    ("HU-10", "Como administrador, quiero registrar los pagos recibidos para conocer en todo "
              "momento el saldo pendiente de cada factura."),
    ("HU-11", "Como administrador, quiero consultar el tablero de control filtrado por "
              "periodo para evaluar el comportamiento del servicio y del recaudo."),
    ("HU-12", "Como supervisor, quiero exportar un reporte a CSV o PDF para analizarlo fuera "
              "del sistema y presentarlo a la gerencia."),
    ("HU-13", "Como administrador, quiero definir el rol y la empresa de cada usuario para "
              "que solo acceda a la información que le corresponde."),
    ("HU-14", "Como administrador, quiero consultar el rastro de auditoría para saber quién "
              "realizó una operación determinada y cuándo."),
]

CRONOGRAMA = [
    ("Análisis", "Marzo 2025", "Levantamiento de requisitos"),
    ("Análisis", "Abril 2025", "Identificación de actores"),
    ("Análisis", "Mayo – junio 2025", "Análisis del problema y evaluación de requisitos"),
    ("Planeación", "Julio 2025", "Diseño de la solución"),
    ("Planeación", "Agosto 2025", "Definición de la arquitectura del sistema"),
    ("Planeación", "Septiembre 2025", "Modelado de casos de uso, diagramas y base de datos"),
    ("Planeación", "Octubre 2025", "Planificación del desarrollo y conformación del backlog"),
    ("Ejecución", "Noviembre 2025", "Sprints 1 y 2, seguridad, acceso y catálogos"),
    ("Ejecución", "Diciembre 2025", "Sprints 3 y 4, motor de emisión y facturación propia"),
    ("Ejecución", "Febrero 2026", "Sprints 5 y 6, clientes API y API de integración"),
    ("Ejecución", "Marzo 2026", "Sprints 7 y 8, consumo y planes, tablero y reportes"),
    ("Ejecución", "Abril 2026", "Integración de módulos"),
    ("Ejecución", "Mayo 2026", "Pruebas técnicas del software"),
    ("Evaluación", "Junio 2026", "Pruebas finales y corrección de errores"),
    ("Evaluación", "Julio 2026", "Socialización y sustentación del proyecto"),
]

# Los no funcionales que se llevan al documento de grado, por su código en E1.
RNF_SELECCIONADOS = ["RNF 01", "RNF 04", "RNF 05", "RNF 07", "RNF 08", "RNF 10", "RNF 11",
                     "RNF 12", "RNF 13", "RNF 14", "RNF 23", "RNF 24", "RNF 26", "RNF 29"]


def _criticos(requisitos):
    return [(c, n, desc, actor, prioridad(v, u))
            for c, n, desc, actor, v, u in requisitos if prioridad(v, u) == "Crítica"]


def escribir(d):
    d.titulo("Capítulo 4. Análisis y especificación de requisitos", nivel=1, nueva_pagina=True)
    _stakeholders(d)
    _historias(d)
    _cronograma(d)
    _funcionales(d)
    _no_funcionales(d)
    _priorizacion(d)


def _stakeholders(d):
    d.titulo("4.1 Matriz de stakeholders", nivel=2)
    d.parrafo(
        "La matriz de stakeholders se empleó para identificar y clasificar a los actores "
        "involucrados en el proyecto según dos criterios:"
    )
    d.vinetas([
        ("Influencia", "capacidad que tiene un actor para afectar las decisiones o el "
                       "desarrollo del proyecto."),
        ("Interés", "nivel de preocupación o participación que tiene respecto de los "
                    "resultados del proyecto."),
    ])
    d.parrafo(
        "El cruce de ambos criterios define cuatro cuadrantes, y cada uno determina una "
        "estrategia distinta de comunicación y de gestión."
    )
    d.figura(
        "Matriz de influencia e interés de las partes interesadas",
        IMAGENES / "FIG-stakeholders.png",
        nota="Elaboración propia. Cada cuadrante determina la estrategia de gestión de los "
             "actores que contiene.",
    )
    d.parrafo(
        "La clasificación arroja una consecuencia que conviene señalar. La administración "
        "tributaria quedó situada en el cuadrante de alta influencia y bajo interés, pues no "
        "participa en el proyecto ni se ve afectada por su éxito, pero fija las condiciones "
        "que todo documento debe cumplir, y un cambio en su normativa obliga a modificar el "
        "sistema. La estrategia frente a ella no es de participación sino de vigilancia, y consiste en "
        "mantenerse informado de sus resoluciones."
    )
    d.parrafo(
        "Los proveedores de software de punto de venta y ERP ocupan el mismo cuadrante por una "
        "razón distinta. Son quienes en la práctica realizan la integración con la "
        "plataforma, de modo que su disposición determina si una empresa cliente puede o no "
        "adoptar el servicio; sin embargo, el resultado del proyecto no les representa un "
        "interés propio. De ahí que el esfuerzo dedicado a que la integración sea sencilla y "
        "esté documentada de forma automática no sea un detalle técnico, sino la estrategia de "
        "gestión de ese grupo de interesados."
    )


def _historias(d):
    d.titulo("4.2 Historias de usuario", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Las historias de usuario expresan las necesidades identificadas desde la perspectiva "
        "de quien las tiene, indicando el actor, lo que necesita y para qué lo necesita. Esta "
        "última parte es la que orienta el diseño, porque dos soluciones pueden satisfacer la "
        "misma "
        "petición y solo una atender el propósito que hay detrás."
    )
    d.tabla(
        "Historias de usuario del sistema",
        ["ID", "Historia de usuario"],
        [[i, h] for i, h in HISTORIAS],
        nota="Elaboración propia. Las historias se redactaron a partir de los hallazgos de la "
             "encuesta y de la observación directa descritos en el capítulo anterior.",
        anchos=[1.7, 14.6],
    )
    d.parrafo(
        "Dos de estas historias no provienen de una petición sino de un hallazgo. La HU-04, "
        "sobre reenviar una emisión sin duplicarla, responde a que el sistema que integra "
        "puede perder la respuesta por una falla de red y volver a intentarlo; sin esa "
        "garantía, el reintento produciría dos facturas del mismo hecho económico. La HU-06, "
        "sobre la recepción del documento por parte del comprador, corresponde a un actor que "
        "no opera el sistema y que por lo mismo nunca habría formulado la petición, pero que "
        "es quien recibe el resultado de todo el proceso."
    )
    d.parrafo(
        "A partir de estas historias se construyó el product backlog y se derivaron los "
        "requisitos funcionales que conforman cada uno de los módulos del sistema."
    )


def _cronograma(d):
    d.titulo("4.3 Cronograma de actividades", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Con el fin de organizar la ejecución del proyecto se estableció un cronograma que "
        "abarca desde el levantamiento de requisitos hasta la socialización del trabajo "
        "final. La planificación se estructuró en cuatro fases, que son análisis, planeación, "
        "ejecución y evaluación, cada una con actividades y entregables definidos, lo que "
        "permitió hacer seguimiento al avance y controlar los tiempos de desarrollo."
    )
    d.tabla(
        "Cronograma de actividades del proyecto",
        ["Fase", "Periodo", "Actividad"],
        [[f, p, a] for f, p, a in CRONOGRAMA],
        nota="Elaboración propia. Los ocho sprints descritos en el capítulo anterior "
             "corresponden a la fase de ejecución, entre noviembre de 2025 y marzo de 2026.",
        anchos=[2.8, 3.8, 9.7],
    )
    d.parrafo(
        "La fase de análisis ocupó cuatro meses, una proporción alta frente al total del "
        "proyecto. La razón es la que se expuso en el capítulo anterior, y es que la elicitación "
        "no "
        "buscaba una lista de funcionalidades sino la causa por la cual empresas obligadas a "
        "facturar no lo estaban haciendo. Establecer que la barrera era el reemplazo del "
        "software, y no el costo ni el desconocimiento, cambió por completo la solución que se "
        "construyó después."
    )


def _funcionales(d):
    d.titulo("4.4 Requisitos funcionales", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Los requisitos funcionales describen las funcionalidades que el sistema debe "
        "proporcionar para satisfacer las necesidades identificadas durante el levantamiento. "
        "Se agruparon en ocho módulos funcionales que corresponden a los conjuntos de trabajo "
        "reales de la plataforma."
    )
    d.parrafo(
        "La agrupación se aparta de la de un sistema comercial convencional, y la diferencia "
        "es deliberada: FactuGest no administra mercancía ni compras a proveedores. Administra "
        "la emisión de documentos por cuenta de terceros y la suscripción con la que ese "
        "servicio se cobra. Donde un sistema de punto de venta tendría gestión de inventario y "
        "gestión de compras, aquí hay gestión de clientes API y gestión de consumo y planes."
    )

    criticos = {codigo: _criticos(reqs) for codigo, _, _, _, reqs in MODULOS}
    total_criticos = sum(len(v) for v in criticos.values())
    total = sum(len(reqs) for *_, reqs in MODULOS)

    d.parrafo(
        f"El levantamiento produjo {total} requisitos funcionales. En este capítulo se "
        f"presentan los {total_criticos} de prioridad crítica, que son aquellos sin los cuales "
        "el sistema no cumple su propósito; el catálogo completo se encuentra en el documento "
        "de especificación de requisitos que se anexa."
    )
    d.tabla(
        "Módulos funcionales y distribución de los requisitos",
        ["Código", "Módulo", "Requisitos", "De prioridad crítica"],
        [[c, n, str(len(reqs)), str(len(criticos[c]))] for c, n, _, _, reqs in MODULOS]
        + [["", "Total", str(total), str(total_criticos)]],
        nota="Elaboración propia.",
        anchos=[2.0, 7.6, 3.2, 3.5],
    )

    for indice, (codigo, nombre, intro, _, _) in enumerate(MODULOS, start=1):
        d.titulo(f"4.4.{indice} {nombre}", nivel=3, nueva_pagina=(indice > 1))
        d.parrafo(intro)
        d.tabla(
            f"Requisitos funcionales críticos del módulo {codigo}",
            ["Código", "Requisito", "Descripción", "Actor"],
            [[c, n, desc, actor] for c, n, desc, actor, _ in criticos[codigo]],
            nota="Elaboración propia. Se relacionan únicamente los requisitos de prioridad "
                 "crítica; los de prioridad alta, media y baja constan en el documento de "
                 "especificación.",
            anchos=[1.7, 3.6, 8.0, 3.0],
        )


def _no_funcionales(d):
    d.titulo("4.5 Requisitos no funcionales", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Los requisitos no funcionales establecen las condiciones de calidad que el sistema "
        "debe satisfacer. No describen funcionalidades, sino restricciones sobre la manera en "
        "que estas se prestan, esto es, con qué rapidez, con qué garantías de seguridad, con qué "
        "integridad de la información y con qué facilidad de mantenimiento."
    )
    d.parrafo(
        "Cada requisito se acompaña de la forma en que se comprueba. Un requisito no funcional "
        "que no indica cómo verificarse es una aspiración y no un requisito, porque al evaluar el "
        "sistema no habría manera de afirmar si se cumplió o no."
    )
    seleccion = [r for r in RNF if r[0] in RNF_SELECCIONADOS]
    d.tabla(
        "Requisitos no funcionales del sistema",
        ["Código", "Categoría", "Requisito", "Verificación"],
        [[c, cat, req, ver] for c, cat, req, ver in seleccion],
        nota=f"Elaboración propia. Se presentan {len(seleccion)} de los {len(RNF)} requisitos "
             "no funcionales especificados; los restantes constan en el documento de "
             "especificación.",
        anchos=[1.7, 2.6, 6.9, 5.1],
    )
    d.parrafo(
        "Tres de estas categorías merecen una observación. Las de integridad de los datos y "
        "trazabilidad no son exigencias genéricas de calidad. Un consecutivo repetido es un "
        "documento rechazado por la administración tributaria, y un rastro de operaciones que "
        "puede editarse no sirve como rastro. La de cumplimiento normativo recoge obligaciones "
        "legales cuyo incumplimiento no degrada el servicio sino que lo invalida."
    )


def _priorizacion(d):
    d.titulo("4.6 Priorización de requisitos funcionales", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Con el fin de establecer el orden de implementación de las funcionalidades, se "
        "priorizaron los requisitos considerando su valor para el negocio y la urgencia "
        "asociada a cada uno. La evaluación empleó una escala de 1 a 5 en ambos criterios, "
        "donde los valores más altos representan un mayor impacto para la organización y una "
        "necesidad más inmediata de implementación."
    )
    d.tabla(
        "Escala de valoración empleada",
        ["#", "Valor de negocio", "Urgencia"],
        [
            ["1", "Impacto muy bajo para la operación", "No es urgente, puede esperar"],
            ["2", "Impacto bajo, aporta poca funcionalidad",
             "Poco urgente, puede desarrollarse después"],
            ["3", "Impacto medio, mejora procesos importantes",
             "Urgencia moderada, conviene implementarlo pronto"],
            ["4", "Impacto alto, necesario para operar con eficiencia",
             "Muy urgente, afecta procesos importantes"],
            ["5", "Impacto crítico, indispensable para el sistema",
             "Urgencia crítica, debe implementarse de inmediato"],
        ],
        nota="Elaboración propia, adaptada de la técnica de priorización por valor y urgencia.",
        anchos=[1.0, 7.6, 7.7],
    )
    d.parrafo(
        "El puntaje individual de cada requisito pondera el valor de negocio en un sesenta por "
        "ciento y la urgencia en un cuarenta por ciento. La ponderación responde a una "
        "decisión explícita, y es que lo importante debe pesar más que lo afanado, porque un "
        "requisito "
        "urgente pero de bajo valor desplaza recursos de otro que sostiene la operación. El "
        "puntaje del módulo es el promedio de los puntajes de sus requisitos."
    )

    filas = []
    for codigo, nombre, _, _, reqs in MODULOS:
        global_modulo = round(sum(puntaje(v, u) for *_, v, u in reqs) / len(reqs), 1)
        criticos = len(_criticos(reqs))
        filas.append((global_modulo, [codigo, nombre, str(len(reqs)), str(criticos),
                                      f"{global_modulo}"]))
    filas.sort(key=lambda x: -x[0])

    d.tabla(
        "Priorización de los módulos funcionales",
        ["Código", "Módulo", "Requisitos", "Críticos", "Puntaje"],
        [fila for _, fila in filas],
        nota="Elaboración propia. Ordenados de mayor a menor puntaje. El detalle requisito por "
             "requisito consta en el documento de especificación.",
        anchos=[1.9, 7.0, 2.6, 2.3, 2.5],
    )

    mayor, menor = filas[0][1][1], filas[-1][1][1]
    d.parrafo(
        f"El orden resultante confirma la naturaleza del proyecto. Encabeza la lista el módulo "
        f"de {mayor.lower()}, del que depende que un documento salga correctamente expedido, y "
        f"cierra el de {menor.lower()}, que agrupa parámetros que se ajustan de vez en cuando. "
        "Entre uno y otro se ordenan los módulos que hacen posible que el cliente emita y que "
        "el servicio se cobre."
    )
    d.parrafo(
        "Conviene distinguir esta priorización del orden en que los módulos se construyeron. "
        "El módulo de emisión es el de mayor puntaje, pero no fue el primero en desarrollarse, porque "
        "sin el catálogo de empresas emisoras no hay resolución de la cual reservar un número. "
        "La prioridad indica qué es más importante; las dependencias técnicas indican qué "
        "puede hacerse antes, y no siempre coinciden."
    )
    d.parrafo(
        "Finalmente, la priorización mantiene correspondencia con los objetivos específicos "
        "del proyecto. Los cinco objetivos enunciados en el capítulo 1 se sostienen sobre los "
        "módulos mejor puntuados, de modo que el orden de implementación adoptado condujo "
        f"directamente a su cumplimiento, tal como se documenta en el capítulo 6. Los "
        f"{len(OBJETIVOS_ESPECIFICOS)} objetivos específicos cuentan cada uno con al menos un "
        "módulo y un conjunto de requisitos que los respaldan."
    )
