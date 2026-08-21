"""
E4 — Preliminares: cubierta, portada, tabla de contenido, resumen, abstract e
introducción.

El resumen y la introducción se escribieron contra el sistema construido y no
contra el planteamiento inicial. Es la primera vez que el documento le dice al
lector qué es FactuGest, y decirlo mal aquí obliga a corregirlo en los seis
capítulos siguientes: no es un facturador de escritorio ni un punto de venta, es un
proveedor que emite por cuenta de terceros y cobra por volumen.
"""
from docx.enum.text import WD_ALIGN_PARAGRAPH

TITULO = "FACTUGEST"
SUBTITULO = ("Plataforma web de facturación electrónica para la emisión de documentos por "
             "cuenta de terceros mediante una API de integración")

INTEGRANTES = ["BRANDON ARLEY RESTREPO GÉLVEZ",
               "JOHAN SEBASTIÁN ACOSTA SÁNCHEZ",
               "WILMER JESÚS CONTRERAS RANGEL"]

FICHA = "3115426"
PROGRAMA = "Tecnólogo en Análisis y Desarrollo de Software"
CENTRO = "Centro de la Industria, la Empresa y los Servicios (CIES)"
CIUDAD = "CÚCUTA, NORTE DE SANTANDER"
ANIO = 2026


def escribir(d):
    _cubierta(d)
    _portada(d)
    d.tabla_contenido()
    _resumen(d)
    _abstract(d)
    _introduccion(d)


def _centrado(d, texto, negrita=False):
    return d.parrafo(texto, sangria=False, alineacion=WD_ALIGN_PARAGRAPH.CENTER,
                     negrita=negrita)


def _cubierta(d):
    """Primera hoja, con el programa de formación y el nombre del proyecto."""
    _centrado(d, "ANÁLISIS Y DESARROLLO DE SOFTWARE", negrita=True)
    for _ in range(3):
        d.parrafo()
    _centrado(d, "INTEGRANTES:")
    for integrante in INTEGRANTES:
        _centrado(d, integrante)
    for _ in range(3):
        d.parrafo()
    _centrado(d, TITULO, negrita=True)
    for _ in range(4):
        d.parrafo()
    _centrado(d, CIUDAD)
    _centrado(d, "SENA — CIES")
    _centrado(d, str(ANIO))
    d.salto_pagina()


def _portada(d):
    """Segunda hoja: el título completo y la finalidad del trabajo."""
    _centrado(d, TITULO, negrita=True)
    _centrado(d, SUBTITULO)
    d.parrafo()
    _centrado(d, "Presentado por:")
    for integrante in INTEGRANTES:
        _centrado(d, integrante)
    d.parrafo()
    _centrado(d, f"Ficha {FICHA}")
    d.parrafo()
    _centrado(d, "Trabajo de grado presentado como requisito para optar al título de:")
    _centrado(d, PROGRAMA)
    d.parrafo()
    _centrado(d, "SERVICIO NACIONAL DE APRENDIZAJE — SENA")
    _centrado(d, CENTRO)
    _centrado(d, PROGRAMA)
    d.parrafo()
    _centrado(d, CIUDAD)
    _centrado(d, str(ANIO))
    d.salto_pagina()


def _resumen(d):
    d.titulo("RESUMEN", nivel=1)
    d.parrafo(
        "El presente proyecto tiene como propósito el análisis, diseño y desarrollo de "
        "FactuGest, una plataforma web de facturación electrónica que opera como proveedor "
        "tecnológico para micro, pequeñas y medianas empresas de Colombia. La propuesta surge "
        "de una barrera concreta: la facturación electrónica es de obligatorio cumplimiento, "
        "pero la mayoría de estas empresas ya opera con un software propio —un punto de "
        "venta, un sistema contable o una aplicación hecha a la medida— y adoptar la "
        "obligación por la vía habitual implica reemplazarlo, con el costo, la curva de "
        "aprendizaje y la interrupción de la operación que ello supone. FactuGest resuelve "
        "esa situación emitiendo por cuenta de la empresa a través de una API de integración "
        "que su propio sistema consume, de modo que el negocio cumple sin cambiar la "
        "herramienta con la que trabaja. La plataforma expide facturas de venta, notas "
        "crédito y notas débito, calcula de forma automática bases gravables, descuentos y "
        "prorrateo de impuestos, reserva el consecutivo autorizado de la resolución, genera "
        "el código único de facturación electrónica, la representación gráfica en PDF y el "
        "archivo XML bajo el estándar UBL 2.1, y hace llegar el documento al comprador. "
        "Administra además el negocio del proveedor: el registro de las empresas integradas, "
        "la llave con la que cada una accede, el plan de suscripción contratado, el control "
        "de su consumo mensual contra el cupo de ese plan y la facturación de la mensualidad "
        "correspondiente, sobre la cual construye un tablero de control y siete reportes "
        "exportables. El proyecto se desarrolló bajo la metodología ágil Scrum, aplicando "
        "encuestas y observación directa como técnicas de elicitación de requisitos, a partir "
        "de las cuales se definieron ochenta y dos requisitos funcionales, treinta y dos no "
        "funcionales y cincuenta y seis casos de uso. La solución se construyó sobre una "
        "arquitectura por capas con Python y FastAPI, plantillas Jinja2 y base de datos "
        "MySQL, con la lógica de negocio concentrada en una capa de servicios que alimenta "
        "por igual a la aplicación web y a la interfaz de integración."
    )
    d.parrafo()
    p = d.parrafo(sangria=False)
    p.add_run("Palabras clave: ").bold = True
    p.add_run("facturación electrónica, API de integración, proveedor tecnológico, DIAN, "
              "UBL 2.1, middleware, suscripción por volumen.")
    d.salto_pagina()


def _abstract(d):
    d.titulo("ABSTRACT", nivel=1)
    d.parrafo(
        "The purpose of this project is the analysis, design, and development of FactuGest, a "
        "web-based electronic invoicing platform that operates as a technology provider for "
        "micro, small, and medium-sized enterprises in Colombia. The proposal addresses a "
        "specific barrier: electronic invoicing is mandatory, yet most of these businesses "
        "already run their own software —a point of sale, an accounting system, or a custom "
        "application— and complying through the usual route means replacing it, with the "
        "associated cost, learning curve, and disruption of daily operations. FactuGest "
        "resolves this by issuing documents on behalf of the company through an integration "
        "API that the company's own system consumes, so the business complies without "
        "changing the tool it works with. The platform issues sales invoices, credit notes, "
        "and debit notes; automatically calculates taxable bases, discounts, and tax "
        "proration; reserves the authorized sequential number from the tax resolution; "
        "generates the unique electronic invoicing code, the PDF representation, and the XML "
        "file under the UBL 2.1 standard; and delivers the document to the buyer. It also "
        "manages the provider's own business: registration of integrated companies, the key "
        "each one uses to authenticate, the subscription plan contracted, the monitoring of "
        "monthly consumption against that plan's quota, and the billing of the corresponding "
        "monthly fee, upon which it builds a control dashboard and seven exportable reports. "
        "The project was developed using the Scrum agile methodology, applying surveys and "
        "direct observation as requirements elicitation techniques, from which eighty-two "
        "functional requirements, thirty-two non-functional requirements, and fifty-six use "
        "cases were defined. The solution was built on a layered architecture using Python "
        "and FastAPI, Jinja2 templates, and a MySQL database, with business logic "
        "concentrated in a service layer that feeds both the web application and the "
        "integration interface."
    )
    d.parrafo()
    p = d.parrafo(sangria=False)
    p.add_run("Keywords: ").bold = True
    p.add_run("electronic invoicing, integration API, technology provider, DIAN, UBL 2.1, "
              "middleware, volume-based subscription.")
    d.salto_pagina()


def _introduccion(d):
    d.titulo("INTRODUCCIÓN", nivel=1)
    d.parrafo(
        "La facturación electrónica dejó de ser en Colombia una opción de modernización para "
        "convertirse en una obligación tributaria exigible. Su incumplimiento no es una "
        "omisión menor: compromete la deducibilidad de costos y gastos, dificulta las "
        "relaciones comerciales con clientes que exigen un soporte válido y expone al "
        "contribuyente a sanciones. Sin embargo, la carga que impone no se distribuye por "
        "igual. Una empresa grande incorpora la obligación en un sistema que ya administra "
        "sus procesos; un negocio pequeño se encuentra con una exigencia técnica que no sabe "
        "cómo atender y con un costo que no tenía previsto."
    )
    d.parrafo(
        "El diagnóstico que dio origen a este proyecto encontró que la dificultad principal "
        "no era la falta de una herramienta de facturación, sino algo distinto: la mayoría de "
        "estos negocios ya opera con un software propio. Un punto de venta en la tienda, un "
        "sistema contable en la oficina, una aplicación hecha a la medida años atrás. Adoptar "
        "la facturación electrónica por la vía habitual —un sistema nuevo que la incluya— "
        "significa reemplazar esa herramienta, capacitar de nuevo al personal e interrumpir "
        "la operación mientras tanto. La barrera no es tecnológica sino de reemplazo, y por "
        "eso una solución que exija cambiar de software no la resuelve: la traslada."
    )
    d.parrafo(
        "En respuesta a esa situación surge FactuGest, una plataforma web que opera como "
        "proveedor tecnológico de facturación electrónica. En lugar de sustituir el sistema "
        "de la empresa, se conecta con él: expone una interfaz de integración que el software "
        "existente consume para enviar los datos de una venta, y FactuGest se encarga de "
        "expedir el documento electrónico con su numeración autorizada, su código único, su "
        "representación gráfica y su archivo XML, y de hacerlo llegar al comprador. La "
        "empresa cumple con la obligación conservando la herramienta con la que trabaja."
    )
    d.parrafo(
        "Prestar ese servicio implica administrarlo. La plataforma incorpora, junto al motor "
        "de emisión, los módulos que sostienen el negocio del proveedor: el registro de las "
        "empresas integradas y de la llave con que cada una se identifica, los planes de "
        "suscripción por volumen de documentos, el control del consumo mensual contra el cupo "
        "contratado y la facturación de la mensualidad correspondiente. Sobre esa operación "
        "se construyeron un tablero de control y un conjunto de reportes exportables que "
        "permiten evaluar tanto la prestación del servicio como su recaudo."
    )
    d.parrafo(
        "El desarrollo se fundamentó en conceptos relacionados con la facturación electrónica "
        "y su normativa, los estándares de documentos comerciales en formato XML, las "
        "arquitecturas orientadas a servicios y el modelo de integración por middleware, la "
        "seguridad en la autenticación de sistemas, el diseño de bases de datos relacionales "
        "y los modelos de negocio basados en suscripción. Estos elementos proporcionaron el "
        "marco conceptual y tecnológico necesario para diseñar una solución que respondiera "
        "al problema identificado."
    )
    d.parrafo(
        "Para asegurar que la solución atendiera necesidades reales y no supuestas, se "
        "aplicaron técnicas de elicitación de requisitos basadas en encuestas dirigidas a "
        "empresas obligadas a facturar electrónicamente y en observación directa de su "
        "operación. La información recopilada permitió establecer ochenta y dos requisitos "
        "funcionales y treinta y dos no funcionales, a partir de los cuales se definieron los "
        "actores, los casos de uso, las historias de usuario y los módulos que orientaron la "
        "construcción del sistema."
    )
    d.parrafo(
        "La metodología Scrum se empleó como marco de trabajo para organizar el proyecto, "
        "gestionar el product backlog, planificar las iteraciones y hacer seguimiento al "
        "avance de cada módulo. Su carácter iterativo resultó determinante en un aspecto "
        "concreto: el alcance del proyecto cambió durante el desarrollo. Lo que empezó como "
        "un sistema de facturación para una empresa se convirtió en un proveedor que emite "
        "por cuenta de varias, al comprobarse que el reemplazo del software era la verdadera "
        "barrera. Un marco de trabajo capaz de incorporar ese hallazgo sin desechar lo "
        "construido fue lo que permitió que el cambio de rumbo fuera una corrección y no un "
        "reinicio."
    )
    d.parrafo(
        "El presente documento describe las etapas desarrolladas durante la construcción de "
        "FactuGest: la identificación de la problemática y la definición de los objetivos, el "
        "marco referencial que sustenta la solución, la metodología de desarrollo y las "
        "técnicas de elicitación aplicadas, el análisis y la especificación de los "
        "requisitos, el diseño de la arquitectura y de la base de datos, la implementación de "
        "los módulos y, finalmente, las pruebas realizadas y los resultados obtenidos."
    )
