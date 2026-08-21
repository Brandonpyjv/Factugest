"""
E4 — Capítulo 1. Planteamiento del problema y formulación del proyecto.

Los objetivos van **literal** como quedaron aprobados en el §9 del cuaderno de
trabajo. Son lo que el capítulo 6 declara cumplido: reescribirlos aquí, aunque
fuera para mejorar la redacción, dejaría al documento prometiendo una cosa y
demostrando otra.
"""

OBJETIVO_GENERAL = (
    "Desarrollar FactuGest, una plataforma web de facturación electrónica que opere como "
    "proveedor tecnológico para micro, pequeñas y medianas empresas de Colombia, "
    "permitiéndoles emitir facturas de venta, notas crédito y notas débito conforme a la "
    "normativa de la DIAN a través de una API de integración que se conecta con los sistemas "
    "que ya utilizan."
)

OBJETIVOS_ESPECIFICOS = [
    "Implementar el módulo de emisión de documentos electrónicos que genere facturas de "
    "venta, notas crédito y notas débito con el cálculo automático de bases gravables, "
    "descuentos y prorrateo de IVA, asignando a cada documento su consecutivo autorizado, su "
    "CUFE, su representación gráfica en PDF y su archivo XML bajo el estándar UBL 2.1.",

    "Construir una API REST de integración que exponga los servicios de facturación a "
    "sistemas externos, con autenticación por llave individual, control de cupo por plan y "
    "una forma única de respuesta y de error documentada en OpenAPI.",

    "Desarrollar el módulo de clientes API y planes de suscripción que administre el alta de "
    "empresas integradas, la generación y rotación de sus llaves, el control de su consumo "
    "mensual y la facturación de su mensualidad.",

    "Implementar un panel de control y un módulo de reportes exportables a CSV y PDF que "
    "consoliden la operación del servicio y la situación financiera de la empresa.",

    "Establecer el esquema de seguridad de la plataforma mediante autenticación de usuarios, "
    "roles jerárquicos con control de acceso por ruta y un registro de auditoría de las "
    "operaciones de escritura.",
]

RESTRICCIONES = [
    "El tiempo disponible para el desarrollo está delimitado por el cronograma del programa "
    "de formación.",
    "La emisión en los servicios de producción de la administración tributaria depende de la "
    "habilitación del proveedor, trámite que no está bajo control del equipo. Mientras tanto, "
    "el código único de facturación electrónica se genera en modalidad de pruebas.",
    "La numeración de cada documento depende de una resolución de facturación vigente, con "
    "prefijo y rango autorizados a la empresa emisora. El sistema no puede suplirla.",
    "El proyecto no puede modificar el software de la empresa integrada, de modo que la solución debe "
    "limitarse a ofrecer una interfaz que ese software consuma.",
    "El funcionamiento requiere conexión a internet en los dos extremos, el del proveedor y "
    "el del sistema integrado.",
    "La infraestructura disponible durante el desarrollo corresponde a un entorno local, no a "
    "un servidor de producción con sus condiciones de disponibilidad y respaldo.",
]

LIMITACIONES = [
    "La adopción de la solución exige que la empresa cuente con un sistema capaz de realizar "
    "peticiones HTTP y con alguien que lo ajuste. Un negocio cuyo software no admita "
    "modificaciones no puede integrarse por esta vía.",
    "La entrega del documento al comprador depende de un servicio de correo de terceros, "
    "cuya indisponibilidad el sistema no controla.",
    "El recaudo de las mensualidades se registra manualmente, ya que no se implementó integración "
    "con pasarelas de pago.",
    "El rendimiento del sistema se verificó en condiciones de desarrollo. No fue sometido a "
    "una carga de producción sostenida ni a un número elevado de emisiones simultáneas.",
    "El cliente móvil quedó fuera del alcance de esta versión, al concentrarse el esfuerzo en "
    "la interfaz de integración.",
    "Delegar la facturación en un tercero supone una decisión de confianza que excede lo "
    "técnico. Una empresa puede rechazar la solución por esa razón aunque funcione "
    "correctamente.",
]


def escribir(d):
    d.titulo("Capítulo 1. Planteamiento del problema y formulación del proyecto",
             nivel=1, nueva_pagina=True)

    _problema(d)
    _justificacion(d)
    _restricciones(d)
    _limitaciones(d)
    _objetivos(d)


def _problema(d):
    d.titulo("1.1 Descripción del problema", nivel=2)
    d.parrafo(
        "La facturación electrónica es en Colombia un requisito de obligatorio cumplimiento "
        "para los sujetos definidos por la Dirección de Impuestos y Aduanas Nacionales. El "
        "incumplimiento compromete la deducibilidad de costos y gastos, dificulta las "
        "relaciones comerciales con clientes que exigen un soporte válido y expone al "
        "contribuyente a sanciones. La obligación, sin embargo, no se distribuye por igual. "
        "Una empresa grande la incorpora en el sistema que ya administra sus procesos, "
        "mientras que un negocio pequeño se enfrenta a una exigencia técnica que no sabe cómo "
        "atender y a un costo que no tenía previsto."
    )
    d.parrafo(
        "El diagnóstico realizado sobre micro, pequeñas y medianas empresas de la región "
        "identificó que la dificultad principal no es la ausencia de una herramienta de "
        "facturación, sino la condición en que esa herramienta llega. La mayoría de estos "
        "negocios ya opera con un software propio, sea un punto de venta en el mostrador, un "
        "sistema contable en la oficina o una aplicación desarrollada a la medida años atrás. "
        "Ese software concentra su catálogo, sus clientes, sus precios y la manera en que el "
        "personal aprendió a trabajar."
    )
    d.parrafo(
        "Frente a esa situación, la oferta habitual del mercado consiste en un sistema nuevo "
        "que incluye la facturación electrónica. Adoptarlo implica reemplazar la herramienta "
        "existente, migrar la información, capacitar de nuevo al personal e interrumpir la "
        "operación mientras dura el cambio. El problema, entonces, no es tecnológico sino de "
        "reemplazo, porque la empresa no rechaza facturar electrónicamente sino abandonar el "
        "sistema con el que ya trabaja. Una solución que exija ese cambio no resuelve la "
        "barrera, la traslada."
    )
    d.parrafo(
        "A esta dificultad se suman otras tres, observadas en los negocios que sí intentaron "
        "cumplir. La primera es el desconocimiento de las condiciones técnicas que la "
        "normativa impone, como la numeración autorizada por resolución, el código único por "
        "documento, el "
        "archivo XML bajo un estándar determinado y la entrega al comprador, que no forman "
        "parte del oficio de quien atiende un negocio. La segunda es el costo de las "
        "soluciones disponibles, dimensionado para empresas con volúmenes de facturación muy "
        "superiores. La tercera es que la información que la empresa está obligada a "
        "registrar termina dispersa entre el software propio y el del proveedor de "
        "facturación, sin que ninguno de los dos ofrezca una vista completa de la operación."
    )
    d.parrafo(
        "De lo anterior surge la pregunta que orienta este proyecto. ¿Cómo puede una micro, "
        "pequeña o mediana empresa cumplir con la obligación de facturar electrónicamente "
        "ante la DIAN sin reemplazar el software con el que ya opera y sin asumir el costo "
        "técnico y económico que las soluciones disponibles le imponen?"
    )


def _justificacion(d):
    d.titulo("1.2 Justificación", nivel=2)
    d.parrafo(
        "Se propone el desarrollo de una plataforma que opere como proveedor tecnológico de "
        "facturación electrónica y que se integre con el software que la empresa ya utiliza, "
        "en lugar de sustituirlo. La decisión de operar bajo un modelo de middleware, es decir, "
        "de una "
        "interfaz que se conecta con los sistemas existentes, responde directamente a la "
        "barrera identificada en el diagnóstico, ya que preserva la inversión previa del "
        "empresario, elimina la curva de aprendizaje de un sistema nuevo y evita interrumpir "
        "la operación diaria del negocio."
    )
    d.parrafo(
        "Desde el punto de vista normativo, la solución atiende una necesidad jurídicamente "
        "exigible y con consecuencias económicas directas. Facilitar el cumplimiento no es "
        "una comodidad, sino la diferencia entre un negocio que puede deducir sus costos y "
        "sostener relaciones comerciales formales y otro que queda expuesto a sanciones y "
        "excluido de clientes que exigen soporte válido."
    )
    d.parrafo(
        "En el plano social y económico, las micro, pequeñas y medianas empresas constituyen "
        "la base del aparato productivo colombiano y son, a la vez, las que menos recursos "
        "tienen para asumir la carga técnica de la transformación digital tributaria. Una "
        "solución accesible, cobrada por volumen de documentos y no por licencia, permite que "
        "un negocio pequeño opere en la formalidad en las mismas condiciones técnicas que una "
        "empresa grande. El efecto no se limita al empresario, pues una mayor formalización "
        "fortalece el recaudo y mejora la trazabilidad de las operaciones comerciales."
    )
    d.parrafo(
        "En lo técnico, el modelo elegido reduce el esfuerzo de integración a su mínimo. El "
        "sistema de la empresa envía los datos de una venta y recibe el documento ya emitido, "
        "sin ocuparse de la numeración autorizada, del cálculo tributario, del estándar del "
        "archivo XML ni de la entrega al comprador. Que el contrato de la interfaz se "
        "publique de forma automática permite que quien integra construya su cliente sin "
        "depender de documentación escrita aparte, que es donde suelen aparecer las "
        "discrepancias entre lo documentado y lo que el sistema realmente hace."
    )
    d.parrafo(
        "Desde la gestión empresarial, la solución convierte una obligación tributaria en un "
        "activo de información. Los datos que la empresa está legalmente obligada a "
        "registrar se transforman en indicadores de operación y de cartera sin trabajo "
        "adicional para el usuario, lo que agrega valor más allá del cumplimiento y responde "
        "a una necesidad real de control en negocios que hoy no cuentan con herramientas de "
        "análisis."
    )
    d.parrafo(
        "Finalmente, en el ámbito formativo, el proyecto integra y evidencia las competencias "
        "del programa, entre ellas el levantamiento y la especificación de requisitos, el modelado de casos de "
        "uso, diseño y normalización de bases de datos relacionales, desarrollo de una "
        "aplicación web, diseño e implementación de servicios REST, aplicación de mecanismos "
        "de seguridad, control de versiones y trabajo bajo una metodología ágil. Su "
        "desarrollo sobre un problema real, con normativa vigente y usuarios reales, otorga "
        "al ejercicio un nivel de exigencia equivalente al de un entorno productivo."
    )


def _restricciones(d):
    d.titulo("1.3 Restricciones", nivel=2)
    d.parrafo(
        "Las restricciones son condiciones impuestas al proyecto desde fuera, que delimitan "
        "lo que puede construirse y bajo qué condiciones."
    )
    d.vinetas(RESTRICCIONES)


def _limitaciones(d):
    d.titulo("1.4 Limitaciones", nivel=2)
    d.parrafo(
        "Las limitaciones son alcances que la solución no cubre o factores que restringen sus "
        "resultados. Se declaran de forma explícita porque un sistema que expide documentos "
        "con efectos tributarios no admite ambigüedad sobre lo que hace y lo que no."
    )
    d.vinetas(LIMITACIONES)


def _objetivos(d):
    d.titulo("1.5 Objetivo general", nivel=2)
    d.parrafo(OBJETIVO_GENERAL)

    d.titulo("1.6 Objetivos específicos", nivel=2)
    d.numerada(OBJETIVOS_ESPECIFICOS)
