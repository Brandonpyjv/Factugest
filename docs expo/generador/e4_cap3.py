"""
E4 — Capítulo 3. Metodología de investigación y desarrollo.

Los sprints están alineados con el cronograma del capítulo 4 (fase de ejecución,
noviembre de 2025 a marzo de 2026). Si uno de los dos cambia, el otro tiene que
cambiar con él: un documento que dice que el módulo de reportes se hizo en el
sprint 8 y en el cronograma lo pone en diciembre se contradice a sí mismo.

Las secciones 3.4.1 y 3.5 dependen de la decisión sobre la encuesta y se completan
cuando esa decisión esté tomada.
"""
from pathlib import Path

from e4_cap2 import cita

IMAGENES = Path(__file__).resolve().parent.parent / "entregables" / "diagramas"

SPRINTS = [
    ("Sprint 1", "Seguridad y acceso",
     "Autenticación de usuarios, hash de contraseñas, roles jerárquicos, control de acceso "
     "por ruta y cierre de sesión por inactividad.",
     "RF 7"),
    ("Sprint 2", "Configuración y catálogos",
     "Empresas emisoras con su resolución y su rango, impuestos, descuentos, métodos y "
     "estados de pago, y catálogo de ubicación.",
     "RF 6"),
    ("Sprint 3", "Motor de emisión",
     "Cálculo tributario, reserva atómica del consecutivo, generación del CUFE, del PDF con "
     "el membrete del emisor y del XML bajo UBL 2.1.",
     "RF 2"),
    ("Sprint 4", "Facturación y cartera propias",
     "Catálogo de planes y servicios, clientes, emisión de la factura propia, registro de "
     "pagos y estados de cartera.",
     "RF 4"),
    ("Sprint 5", "Clientes API y llaves",
     "Alta de empresas integradas, generación y rotación de llaves, estados del cliente y "
     "registro en auditoría.",
     "RF 1"),
    ("Sprint 6", "API de integración",
     "Autenticación por llave, validación de la entrada, forma única de error, operaciones de "
     "emisión y consulta, y publicación del contrato en OpenAPI.",
     "RF 8"),
    ("Sprint 7", "Consumo, cupo y planes",
     "Conteo del consumo mensual, bloqueo por cupo agotado, periodo facturable, excedentes y "
     "emisión de la mensualidad por la propia API.",
     "RF 3"),
    ("Sprint 8", "Tablero, reportes y auditoría",
     "Indicadores del servicio y de la venta, filtros de periodo y empresa, los siete "
     "reportes, su exportación y la consulta del rastro de auditoría.",
     "RF 5"),
]

EQUIPO = [
    ("Brandon Arley Restrepo Gélvez", "Product Owner y desarrollador",
     "Definió y priorizó el product backlog, mantuvo la relación con la empresa "
     "colaboradora y desarrolló el motor de emisión y la API de integración."),
    ("Johan Sebastián Acosta Sánchez", "Scrum Master y desarrollador",
     "Facilitó las reuniones del equipo, hizo seguimiento a los impedimentos y desarrolló "
     "los módulos de facturación propia, consumo y planes."),
    ("Wilmer Jesús Contreras Rangel", "Analista y desarrollador",
     "Condujo la elicitación de requisitos y el modelado, y desarrolló los módulos de "
     "seguridad, configuración, tablero y reportes."),
]

INTERESADOS = [
    ("Empresas obligadas a facturar electrónicamente",
     "Usuarios finales del servicio. De su capacidad para integrarse depende que la solución "
     "resuelva el problema planteado."),
    ("Siste Soluciones",
     "Empresa colaboradora con un punto de venta en operación sin facturación electrónica. "
     "Sirvió como caso de integración para verificar que un sistema externo puede emitir a "
     "través de la plataforma."),
    ("Administración tributaria (DIAN)",
     "Fija las condiciones que el documento debe cumplir y habilita a los proveedores "
     "tecnológicos. No participa en el desarrollo, pero determina sus reglas."),
    ("Compradores",
     "Reciben el documento emitido. No operan el sistema, pero son quienes verifican que el "
     "documento llegue y sea legible."),
    ("Equipo de desarrollo",
     "Responsable del análisis, la construcción y las pruebas de la solución."),
    ("Centro de formación e instructores",
     "Orientan el desarrollo del proyecto y evalúan su cumplimiento como trabajo de grado."),
]

PREGUNTAS = [
    ("1", "¿Su empresa está obligada a facturar electrónicamente ante la DIAN?",
     "Sí / No / No lo sé"),
    ("2", "¿Actualmente emite facturación electrónica?", "Sí / No / Está en proceso"),
    ("3", "¿Con qué software administra hoy sus ventas?",
     "Punto de venta / Sistema contable / Aplicación propia / Hojas de cálculo / Ninguno"),
    ("4", "¿Cuántos documentos emite en promedio al mes?",
     "Menos de 50 / 50 a 150 / 151 a 400 / Más de 400"),
    ("5", "¿Cuál ha sido la principal dificultad para adoptar la facturación electrónica?",
     "El costo / Tener que cambiar de software / No saber cómo hacerlo / La capacitación del "
     "personal / Ninguna"),
    ("6", "¿Estaría dispuesto a cambiar el software con el que trabaja hoy para poder "
     "facturar electrónicamente?", "Sí / No / Tal vez"),
    ("7", "Si pudiera seguir usando su software actual y que este emitiera la factura "
     "electrónica automáticamente, ¿le interesaría?", "Sí / No / Tal vez"),
    ("8", "¿Quién se encarga en su empresa de los temas de sistemas?",
     "Un empleado propio / Un técnico externo / El proveedor del software / Nadie"),
    ("9", "¿Qué tan importante considera recibir un soporte oportuno ante un fallo en la "
     "facturación?", "Escala de 1 a 5"),
    ("10", "¿Cuánto estaría dispuesto a pagar mensualmente por el servicio de facturación "
     "electrónica?",
     "Menos de $50.000 / $50.000 a $100.000 / $100.001 a $200.000 / Más de $200.000"),
    ("11", "¿Le interesaría contar con reportes de sus ventas a partir de lo que factura?",
     "Sí / No / Tal vez"),
    ("12", "¿Ha tenido que corregir o anular facturas ya emitidas?",
     "Nunca / Rara vez / Con frecuencia"),
]


def escribir(d):
    d.titulo("Capítulo 3. Metodología de investigación y desarrollo", nivel=1,
             nueva_pagina=True)
    _scrum(d)
    _backlog(d)
    _elicitacion(d)
    _tecnicas(d)
    _equipo(d)


def _scrum(d):
    d.titulo("3.1 Metodología de desarrollo: Scrum", nivel=2)
    d.parrafo(
        "Scrum es un marco de trabajo ágil para el desarrollo de productos complejos, basado "
        "en iteraciones cortas de duración fija llamadas sprints, al término de cada una de "
        f"las cuales se entrega un incremento utilizable del producto ({cita('scrum')}). Su "
        "estructura se apoya en tres artefactos —el product backlog, el sprint backlog y el "
        "incremento— y en eventos de planificación, seguimiento diario, revisión y "
        "retrospectiva."
    )
    d.parrafo(
        "La elección de Scrum para este proyecto no respondió únicamente a su difusión. "
        "Respondió a una condición del problema: al inicio del desarrollo no estaba resuelto "
        "de qué manera la solución llegaría a las empresas. Un marco de trabajo que exigiera "
        "fijar la totalidad de los requisitos antes de construir habría obligado a "
        "comprometerse con esa decisión demasiado pronto."
    )
    d.parrafo(
        "El hecho más importante del proyecto confirma esa elección. Durante el desarrollo se "
        "comprobó que la barrera real no era la ausencia de una herramienta de facturación "
        "sino el reemplazo del software existente, y el proyecto pasó de ser un sistema de "
        "facturación para una empresa a ser un proveedor que emite por cuenta de varias a "
        "través de una API. Ese cambio se incorporó como una reordenación del product "
        "backlog: lo construido —el motor de emisión, el cálculo tributario, la generación "
        "del PDF y del XML— siguió siendo válido, porque el cambio afectó la manera de "
        "ofrecer el servicio y no la manera de expedir un documento. Con un enfoque secuencial "
        "el mismo hallazgo, aparecido a mitad de la construcción, habría implicado rehacer el "
        "análisis completo."
    )
    d.figura(
        "Ciclo de Scrum aplicado al desarrollo de FactuGest",
        IMAGENES / "FIG-scrum.png",
        nota="Elaboración propia con base en Schwaber y Sutherland (2020). Los sprints "
             "tuvieron una duración de dos semanas y cada uno cerró con un módulo utilizable.",
    )
    d.parrafo(
        "Se definieron ocho sprints de dos semanas durante la fase de ejecución. Cada uno se "
        "orientó a dejar un módulo en funcionamiento y no una porción de varios: un módulo "
        "terminado puede mostrarse, probarse y corregirse, mientras que tres módulos a medias "
        "solo pueden describirse."
    )


def _backlog(d):
    d.titulo("3.2 Product backlog", nivel=2)
    d.parrafo(
        "El product backlog se conformó con las funcionalidades identificadas durante la "
        "elicitación, organizadas en los ocho módulos funcionales del sistema y priorizadas "
        "según su valor para el negocio y su urgencia, criterio que se detalla en el capítulo "
        "siguiente. La lista completa comprende ochenta y dos requisitos funcionales."
    )
    d.parrafo(
        "El orden de los sprints no siguió la prioridad de los requisitos sino sus "
        "dependencias técnicas, que es una distinción que conviene explicar. El módulo de "
        "emisión es el de mayor prioridad del proyecto, pero no puede construirse antes que "
        "el catálogo de empresas emisoras: sin una resolución con su prefijo y su rango no "
        "hay número que reservar. De la misma manera, la facturación de las mensualidades se "
        "dejó para el sprint 7 porque se emite a través de la propia API, que solo existió "
        "desde el sprint 6."
    )
    d.tabla(
        "Organización del product backlog en sprints",
        ["Sprint", "Módulo", "Alcance comprometido", "Requisitos"],
        [[s, m, a, r] for s, m, a, r in SPRINTS],
        nota="Elaboración propia. La columna «Requisitos» remite a los módulos del catálogo "
             "de requisitos funcionales especificado en el capítulo 4.",
        anchos=[1.9, 3.3, 8.9, 2.2],
    )


def _elicitacion(d):
    d.titulo("3.3 Elicitación de requisitos", nivel=2)
    d.parrafo(
        "La elicitación de requisitos es la etapa en la que se identifican, comprenden y "
        "documentan las necesidades de los usuarios y las expectativas de los interesados. De "
        "su calidad depende que el sistema resuelva un problema real y no uno supuesto: un "
        "error introducido aquí se propaga al diseño, a la construcción y a las pruebas, y "
        "resulta más costoso de corregir en cada etapa que atraviesa "
        f"({cita('sommerville')})."
    )
    d.parrafo(
        "En este proyecto la elicitación debía responder una pregunta previa a cualquier "
        "listado de funcionalidades: por qué empresas obligadas a facturar electrónicamente "
        "no lo estaban haciendo. Preguntar directamente qué funciones querían en un sistema "
        "de facturación habría producido una lista de funcionalidades convencional y habría "
        "dejado intacta la causa del incumplimiento."
    )
    d.parrafo(
        "Se emplearon dos técnicas complementarias: la encuesta, para conocer la situación de "
        "un conjunto amplio de negocios, y la observación directa, para ver de cerca cómo "
        "opera uno de ellos. La primera indica qué tan extendido está un problema; la "
        "segunda, por qué ocurre."
    )


def _tecnicas(d):
    d.titulo("3.4 Técnicas de elicitación utilizadas", nivel=2)

    d.titulo("3.4.1 Encuesta", nivel=3)
    d.parrafo(
        "Se diseñó un cuestionario dirigido a micro, pequeñas y medianas empresas de la "
        "ciudad, con el propósito de establecer su situación frente a la obligación de "
        "facturar electrónicamente, el software con el que operan actualmente y las razones "
        "por las cuales no han adoptado la facturación electrónica o han tenido dificultades "
        "para hacerlo."
    )
    d.parrafo(
        "El instrumento consta de doce preguntas de respuesta cerrada, agrupadas en cuatro "
        "bloques: situación frente a la obligación, herramientas que utiliza el negocio, "
        "barreras percibidas y disposición frente a una solución que se integre con el "
        "software existente. Las preguntas 6 y 7 son deliberadamente complementarias: la "
        "primera indaga si la empresa cambiaría de software para poder cumplir y la segunda "
        "si le interesaría cumplir sin cambiarlo. Contrastar ambas respuestas es lo que "
        "permite distinguir el rechazo a la facturación electrónica del rechazo al reemplazo "
        "del software, que son cosas distintas y conducen a soluciones distintas."
    )
    d.tabla(
        "Instrumento de encuesta aplicado",
        ["N.º", "Pregunta", "Opciones de respuesta"],
        [[n, p, o] for n, p, o in PREGUNTAS],
        nota="Elaboración propia. Cuestionario de respuesta cerrada, diligenciado en "
             "formulario digital.",
        anchos=[1.2, 8.4, 6.7],
    )

    d.titulo("3.4.2 Observación directa", nivel=3)
    d.parrafo(
        "La observación directa se realizó sobre la operación de Siste Soluciones, una "
        "empresa que administra sus ventas con un punto de venta propio y que no emite "
        "facturación electrónica. La técnica consistió en presenciar el registro de ventas "
        "durante la jornada, sin intervenir en el proceso, y en revisar con el responsable el "
        "recorrido completo de una venta desde que se registra hasta que se entrega el "
        "comprobante."
    )
    d.parrafo(
        "La observación permitió establecer cuatro hechos que una encuesta no habría "
        "revelado. El primero es que el punto de venta concentra información que el negocio "
        "no está dispuesto a migrar: catálogo, precios, clientes frecuentes y una forma de "
        "operar que el personal domina. El segundo es que el registro de una venta toma pocos "
        "segundos, de modo que cualquier solución que agregue pasos al proceso de venta será "
        "rechazada por el operario aunque la gerencia la apruebe. El tercero es que el "
        "comprobante que hoy se entrega no tiene validez fiscal, pero cumple una función "
        "comercial que el cliente ya espera. El cuarto es que el negocio no cuenta con "
        "personal técnico permanente: cualquier integración debe ser lo bastante simple como "
        "para que la realice quien mantiene el punto de venta."
    )
    d.parrafo(
        "De estos hallazgos se derivaron decisiones concretas del diseño. Que la emisión "
        "ocurra a través de una interfaz que el punto de venta consume —y no de una pantalla "
        "adicional que el cajero deba diligenciar— responde al segundo hallazgo. Que el "
        "contrato de esa interfaz se publique de forma automática y explorable responde al "
        "cuarto. Y que la solución no exija migrar el catálogo ni los clientes del negocio "
        "responde al primero."
    )


def _equipo(d):
    d.titulo("3.7 Equipo de proyecto y partes interesadas", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El equipo de trabajo se conformó con tres integrantes, quienes asumieron los roles "
        "previstos por Scrum sin dejar de participar en el desarrollo. En un equipo de este "
        "tamaño la separación estricta de roles resulta impracticable: lo que se mantuvo fue "
        "la responsabilidad sobre cada función, no la exclusividad en ella."
    )
    d.tabla(
        "Equipo de proyecto y responsabilidades",
        ["Integrante", "Rol", "Responsabilidades"],
        [[i, r, resp] for i, r, resp in EQUIPO],
        nota="Elaboración propia.",
        anchos=[4.4, 3.6, 8.3],
    )
    d.parrafo(
        "Las partes interesadas comprenden a quienes se ven afectados por el proyecto o "
        "influyen en él, participen o no en su construcción. Su identificación temprana "
        "permite anticipar qué se espera de la solución desde cada posición, que no siempre "
        "coincide."
    )
    d.tabla(
        "Partes interesadas del proyecto",
        ["Parte interesada", "Relación con el proyecto"],
        [[p, r] for p, r in INTERESADOS],
        nota="Elaboración propia. La matriz de stakeholders del capítulo 4 detalla su nivel "
             "de interés y de influencia.",
        anchos=[5.0, 11.3],
    )
