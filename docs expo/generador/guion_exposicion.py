"""
Guion de la sustentación, con lo que dice cada expositor en cada diapositiva.

No es un documento académico sino material de trabajo, así que va con interlineado
sencillo para que quepa en pocas hojas y pueda tenerse a mano mientras se ensaya.

El reparto sigue los roles declarados en el capítulo 3 del documento de grado. Que
cada uno hable de lo que le tocó hacer no es solo comodidad: si el jurado pregunta,
responde quien lo construyó.
"""
from pathlib import Path

from apa import DocumentoAPA
from docx.shared import Pt

SALIDA = Path(__file__).resolve().parent.parent / "carpeta exposicion"
ARCHIVO = SALIDA / "FactuGest - Guion de la Sustentación.docx"

REPARTO = [
    ("Brandon Arley Restrepo Gélvez", "Product Owner", "1 a 10",
     "Formulación del proyecto", "8 minutos"),
    ("Wilmer Jesús Contreras Rangel", "Analista", "11 a 25",
     "Análisis, requisitos y casos de uso", "11 minutos"),
    ("Johan Sebastián Acosta Sánchez", "Scrum Master", "26 a 41",
     "Metodología, diseño técnico, desarrollo e implementación", "11 minutos"),
]

# (número, título, qué se ve, qué decir)
BRANDON = [
    (1, "Portada", "El logotipo de FactuGest y los nombres del equipo.",
     "Buenos días. Somos Brandon Restrepo, Johan Acosta y Wilmer Contreras, de la ficha "
     "3115426. Presentamos FactuGest, nuestro proyecto de grado. Yo abro con el "
     "planteamiento, Wilmer continúa con el análisis y Johan cierra con el desarrollo y las "
     "pruebas."),
    (2, "FactuGest", "El nombre del proyecto y una línea que lo define.",
     "FactuGest es una plataforma web de facturación electrónica, pero con una diferencia "
     "que es la que da sentido a todo el proyecto. No le vendemos un sistema a la empresa "
     "para que reemplace el suyo. Emitimos por cuenta de ella, desde el software que ya "
     "está usando."),
    (3, "I. Formulación del proyecto", "Diapositiva divisoria.",
     "Empiezo entonces por el problema que encontramos."),
    (4, "Planteamiento del Problema", "Tres puntos sobre la barrera de adopción.",
     "La facturación electrónica es obligatoria en Colombia y su incumplimiento tiene "
     "consecuencias reales. Sin embargo, la mayoría de las mipymes todavía no la ha "
     "adoptado. Cuando fuimos a mirar por qué, encontramos algo que no esperábamos. Estas "
     "empresas ya tienen su propio software, un punto de venta, un sistema contable o algo "
     "hecho a la medida hace años, y ahí está su catálogo, sus precios y la forma en que su "
     "gente aprendió a trabajar. Lo que el mercado les ofrece es un sistema nuevo que "
     "incluye la facturación, o sea, cambiar de herramienta. Por eso decimos que el problema "
     "no es tecnológico sino de reemplazo. No rechazan facturar, rechazan cambiar."),
    (5, "Justificación del Proyecto", "Tres cifras de la encuesta y la frase de cierre.",
     "Estas tres cifras salen de la encuesta que aplicamos y que Wilmer va a detallar más "
     "adelante. El 82 % de las empresas está obligada a facturar electrónicamente. El 38 % "
     "señala el cambio de software como su principal barrera, por encima del costo. Y el "
     "84 % lo haría si no tuviera que cambiar de herramienta. Ahí está la oportunidad, y de "
     "ahí sale nuestra propuesta."),
    (6, "Objetivo General", "El objetivo completo, centrado.",
     "Nuestro objetivo general es desarrollar FactuGest, una plataforma web de facturación "
     "electrónica que opere como proveedor tecnológico para las mipymes colombianas, "
     "permitiéndoles emitir facturas de venta, notas crédito y notas débito conforme a la "
     "normativa de la DIAN, a través de una API de integración que se conecta con los "
     "sistemas que ya utilizan."),
    (7, "Objetivos Específicos", "Los cinco objetivos numerados.",
     "De ese objetivo salen cinco específicos. El primero es el motor de emisión, con el "
     "cálculo tributario, el consecutivo, el CUFE, el PDF y el XML. El segundo es la API de "
     "integración. El tercero es el módulo de clientes y planes, que es el que sostiene el "
     "negocio. El cuarto es el tablero y los reportes. Y el quinto es la seguridad, con "
     "roles y auditoría. Los cinco están cumplidos y Johan lo va a mostrar al final."),
    (8, "Alcance", "Dos columnas, lo que hace y lo que no.",
     "Es importante ser claros con el alcance. A la izquierda está lo que el sistema hace "
     "hoy, funcionando. A la derecha lo que dejamos fuera, y quiero detenerme en el primer "
     "punto. La transmisión a los servicios de producción de la DIAN depende de una "
     "habilitación como proveedor tecnológico, que es un trámite que no controlamos. El "
     "sistema está construido para ese momento, pero el código único hoy se genera en "
     "modalidad de pruebas."),
    (9, "Riesgos y Restricciones", "Dos bloques de tres puntos cada uno.",
     "Los riesgos que identificamos son tres. Que la empresa no tenga quién le haga la "
     "integración, que un servicio externo como el correo falle, y uno que no es técnico "
     "pero pesa, que la empresa desconfíe de entregarle su facturación a un tercero. Las "
     "restricciones son las condiciones que no dependen de nosotros, sobre todo la "
     "habilitación ante la DIAN."),
    (10, "Cronograma de Actividades", "Tabla con las cuatro fases.",
     "El proyecto tomó dieciséis meses, de marzo de 2025 a julio de 2026, en cuatro fases. "
     "Quiero señalar que el análisis ocupó cuatro meses, que es bastante, y fue a propósito, "
     "porque de ahí salió el hallazgo que cambió la solución. Con eso le paso la palabra a "
     "Wilmer."),
]

WILMER = [
    (11, "II. Análisis", "Diapositiva divisoria.",
     "Gracias. Yo estuve a cargo del levantamiento de requisitos y del modelado, así que "
     "les voy a contar cómo llegamos a lo que Brandon acaba de plantear."),
    (12, "Herramientas para la Captura de Requisitos (Encuesta)", "La gráfica de las preguntas 6 y 7.",
     "Aplicamos una encuesta de doce preguntas cerradas a 45 empresas de Cúcuta. Las dos "
     "preguntas que ven aquí son el corazón del proyecto y las diseñamos para que fueran "
     "complementarias. A la izquierda preguntamos si cambiarían de software para poder "
     "facturar, y el 58 % dijo que no. A la derecha preguntamos si les interesaría facturar "
     "sin cambiar de software, y el 84 % dijo que sí. Son las mismas empresas. Lo que "
     "rechazan no es la facturación electrónica, es el cambio de herramienta."),
    (13, "Historias de Usuario", "Tres historias derivadas de la encuesta.",
     "De ahí salieron estas historias. Me detengo en la segunda, la HU-04, porque no la "
     "pidió nadie. La sacamos de pensar qué pasa si el sistema del cliente envía una factura "
     "y se le cae la conexión antes de recibir la respuesta. Si vuelve a intentarlo sin más, "
     "quedarían dos facturas del mismo hecho económico."),
    (14, "Requisitos Funcionales Relacionados", "Tabla con cuatro requisitos.",
     "Cada historia se convirtió en requisitos concretos. Estos cuatro pertenecen a los "
     "módulos de integración y de documentos electrónicos, que son los que sostienen la "
     "propuesta."),
    (15, "Herramientas para la Captura de Requisitos (Observación directa)", "Cuatro hallazgos de campo.",
     "La segunda técnica fue observación directa. Estuvimos en un punto de venta en "
     "operación, viendo cómo registran sus ventas, sin intervenir. Cuatro cosas que una "
     "encuesta no nos habría dicho. La segunda es la más importante para el diseño, porque "
     "registrar una venta toma segundos y cualquier cosa que agregue pasos la termina "
     "rechazando quien la usa."),
    (16, "Historias de Usuario", "Tres historias del lado del proveedor.",
     "Del lado de quien presta el servicio salieron estas otras, sobre el alta de clientes, "
     "la rotación de llaves y el seguimiento del negocio."),
    (17, "Requisitos Funcionales Relacionados", "Tabla con cuatro requisitos.",
     "Aquí hay una diferencia que vale la pena señalar. La observación no nos dio funciones "
     "nuevas, nos dio condiciones sobre las que ya teníamos. "
     "En eso se diferencian las dos técnicas, porque la encuesta dice qué tan extendido está "
     "un problema y la observación dice por qué ocurre."),
    (18, "Matriz de Stakeholders", "La matriz de influencia e interés.",
     "Clasificamos a los interesados por influencia e interés. Fíjense dónde quedó la DIAN, "
     "en alta influencia y bajo interés. No participa en el proyecto ni le importa si nos va "
     "bien, pero fija todas las condiciones que un documento debe cumplir. Con ella la "
     "estrategia no es involucrarla, es estar pendientes de sus resoluciones."),
    (19, "Técnica de Priorización", "La escala de 1 a 5.",
     "Priorizamos con una escala de uno a cinco en valor de negocio y en urgencia. El "
     "puntaje pondera el valor al 60 % y la urgencia al 40 %, y esa decisión la tomamos a "
     "propósito, porque lo importante debe pesar más que lo afanado."),
    (20, "Conclusión de la Priorización", "Los ocho módulos ordenados por puntaje.",
     "Este es el resultado. Encabeza la gestión de documentos electrónicos, que es de lo que "
     "depende que una factura salga bien expedida, y cierra la configuración, que son "
     "parámetros que se tocan de vez en cuando."),
    (21, "Requisitos Funcionales", "Tabla de los ocho módulos.",
     "En total especificamos 82 requisitos funcionales en ocho módulos, de los cuales 34 son "
     "de prioridad crítica. Quiero que noten los nombres de los módulos, porque ahí se ve "
     "que este no es un sistema comercial. Donde un punto de venta tendría inventario y "
     "compras, nosotros tenemos clientes API y consumo y planes."),
    (22, "Requisitos No Funcionales", "Tabla por categorías.",
     "Y 32 requisitos no funcionales. Cada uno lleva escrito cómo se comprueba, porque un "
     "requisito no funcional que no dice cómo verificarse es una aspiración, no un "
     "requisito."),
    (23, "III. Diseño", "Diapositiva divisoria.",
     "Con los requisitos definidos pasamos al diseño."),
    (24, "Casos de Uso", "El diagrama general.",
     "Identificamos 56 casos de uso en los ocho módulos, con seis actores. Dos de esos "
     "actores no son personas. Uno es el sistema externo que consume nuestra API, que es el "
     "que más documentos origina, y el otro es el comprador, que recibe el documento y nunca "
     "entra al sistema."),
    (25, "Documentación de Casos de Uso", "La ficha de CU-08.",
     "Esta es la ficha del caso central, emitir una factura. Quiero señalar el orden de los "
     "pasos, porque no es casual. El cupo se valida en el paso 3, antes de reservar el número "
     "en el paso 4. Si lo hiciéramos al revés y después rechazáramos la emisión, habríamos "
     "gastado un consecutivo de una resolución autorizada en un documento que nunca existió. "
     "Con esto le paso la palabra a Johan."),
]

JOHAN = [
    (26, "Metodología de Desarrollo", "El ciclo de Scrum.",
     "Gracias. Yo fui el Scrum Master del equipo. Trabajamos con Scrum en ocho sprints de "
     "dos semanas, y cada sprint cerró con un módulo funcionando, no con partes de varios. "
     "Y aquí hay algo que quiero contarles con franqueza, y es que el alcance del proyecto "
     "cambió a mitad del desarrollo. Cuando confirmamos que la barrera era el reemplazo del software, "
     "pasamos de hacer un facturador para una empresa a hacer un proveedor que emite para "
     "varias. Con Scrum eso se absorbió reordenando el backlog, sin botar lo construido, "
     "porque cambió la forma de ofrecer el servicio, no la de expedir un documento."),
    (27, "Mockup del Panel de Control", "El diseño previo del tablero.",
     "Antes de programar diseñamos las dos pantallas más usadas. En el tablero la decisión "
     "de fondo fue qué mostrar primero. Lo partimos en dos secciones y pusimos el servicio "
     "antes que la venta, porque el servicio es lo que la empresa hace y cobrarlo viene "
     "después. Un tablero que abriera con las ventas estaría describiendo un comercio, no un "
     "proveedor de facturación."),
    (28, "Mockup de Crear Nueva Factura", "El formulario en tres pasos.",
     "El formulario lo organizamos en tres momentos, a quién se le factura, qué se le "
     "factura y cómo paga, con el total siempre a la vista. Eso responde directamente al "
     "hallazgo de la observación que mencionó Wilmer."),
    (29, "Diseño de la Base de Datos", "El modelo entidad-relación.",
     "La base tiene 27 tablas organizadas en dos zonas que no se mezclan, más una tabla "
     "puente. La zona comercial guarda lo que nosotros vendemos y la de middleware lo que "
     "emitimos por cuenta de terceros. Esa separación no es un gusto de diseño, porque si un "
     "documento emitido para un cliente se guardara en la zona comercial, el tablero lo "
     "contaría como ingreso nuestro. No daría error, daría cifras equivocadas."),
    (30, "Diccionario de Datos", "Las columnas de la tabla documentos.",
     "Este es el diccionario de la tabla principal. Señalo dos campos. La referencia externa "
     "es la que permite reintentar sin duplicar, y sobre el número hay un índice único por "
     "emisor y tipo, que es la última defensa contra un consecutivo repetido."),
    (31, "IV. Desarrollo", "Diapositiva divisoria.",
     "Paso entonces a cómo se construyó."),
    (32, "Herramientas de Backend", "Tabla con Python, MySQL, web y el entorno.",
     "Del lado del servidor usamos Python con FastAPI, y lo elegimos por dos razones. Valida "
     "los datos de entrada a partir de los tipos declarados, y publica el contrato de la "
     "API automáticamente desde el propio código. Eso significa que la "
     "documentación no se puede desviar de lo que el sistema hace."),
    (33, "Herramientas de Apoyo y Pruebas", "Claude, Postman, Git y pytest.",
     "Como apoyo usamos Postman para probar la API antes de integrarla, Git y GitHub para el "
     "trabajo en equipo, pytest para las pruebas automatizadas, y asistencia de inteligencia "
     "artificial para revisar código y contrastar decisiones de diseño."),
    (34, "V. Implementación", "Diapositiva divisoria.",
     "Y termino con las pruebas y los resultados."),
    (35, "Pruebas del Sistema", "Qué se comprueba y qué quedó fuera.",
     "Tenemos 190 pruebas automatizadas que corren en tres segundos, más las pruebas "
     "funcionales sobre la interfaz. Fíjense en el tipo de cosas que comprobamos, como que un "
     "fallo a mitad de una emisión no gaste un consecutivo, o que el documento lleve la "
     "identidad de la empresa emisora y no la nuestra. En un sistema que expide documentos "
     "con efectos tributarios, comprobar qué pasa cuando algo falla pesa tanto como "
     "comprobar que funciona. También decimos qué quedó fuera, que es la carga sostenida y "
     "la validación contra los servicios de producción de la DIAN."),
    (36, "Evidencia de Pruebas, registro de cliente", "Formulario y resultado del registro.",
     "Esta es una de las cuatro pruebas funcionales documentadas. A la izquierda el "
     "formulario diligenciado y a la derecha el cliente ya registrado y disponible."),
    (37, "Evidencia de Pruebas, emisión de factura", "Formulario y la factura emitida.",
     "Y esta es la prueba central. A la izquierda el formulario de emisión y a la derecha la "
     "factura ya expedida, con su numeración, su código QR, su CUFE y sus totales "
     "calculados. Este es el documento que recibe el comprador."),
    (38, "Resultado Obtenido de la Emisión", "Tabla con lo comprobado.",
     "La prueba fue satisfactoria en los cinco puntos que verificamos. Y quiero cerrar este "
     "punto contándoles una decisión técnica. El consecutivo se reserva dentro de la misma "
     "transacción que guarda el documento, de manera que si algo falla a mitad no queda una "
     "factura incompleta ni se gasta un número de la resolución."),
    (39, "Resultados Obtenidos", "Tabla de cumplimiento de los objetivos.",
     "Los cinco objetivos específicos se cumplieron, con una salvedad que ya mencionamos, la "
     "transmisión en producción. Y la demostración de que esto resuelve el problema la "
     "hicimos con un punto de venta real que no emitía facturación electrónica. Quedó "
     "expidiendo documentos válidos sin que cambiáramos la forma en que registra sus ventas."),
    (40, "Referencias", "Las fuentes principales.",
     "Estas son las fuentes principales del trabajo. Las trece completas están en el "
     "documento, en estilo APA séptima edición."),
    (41, "Cierre", "La diapositiva de agradecimiento.",
     "Con eso terminamos. Muchas gracias por su atención y quedamos atentos a sus "
     "preguntas."),
]

PREGUNTAS = [
    ("¿Por qué no hicieron un sistema de facturación normal?",
     "Porque ya existen y no resuelven el problema que encontramos. La encuesta mostró que "
     "el 58 % de las empresas no cambiaría su software, pero el 84 % facturaría si no "
     "tuviera que cambiarlo. Un sistema más habría sido una opción más que rechazar.",
     "Brandon"),
    ("¿Ya están emitiendo facturas válidas ante la DIAN?",
     "El sistema genera el documento completo, con su numeración autorizada, su CUFE, su PDF "
     "y su XML bajo UBL 2.1. Lo que falta es la habilitación como proveedor tecnológico, que "
     "es un trámite ante la DIAN. Por eso el código único hoy se genera en modalidad de "
     "pruebas, y lo declaramos así en el alcance y en las conclusiones.", "Johan"),
    ("¿Qué pasa si el sistema del cliente envía la misma factura dos veces?",
     "No se duplica. Cada emisión puede traer una referencia externa, que es el "
     "identificador de la venta en el sistema del cliente. Si llega una repetida, "
     "devolvemos el documento que ya expedimos en lugar de crear otro. Eso se llama "
     "idempotencia y fue una decisión temprana.", "Wilmer"),
    ("¿Cómo garantizan que no se repita un número de factura?",
     "De dos formas. El consecutivo se reserva en una sola sentencia, no leyendo y "
     "actualizando por separado, que es donde dos peticiones simultáneas obtendrían el mismo "
     "número. Y además la tabla tiene un índice único por empresa, tipo y número, como "
     "última defensa.", "Johan"),
    ("¿Por qué la base tiene dos tablas de documentos?",
     "Porque son hechos económicos distintos. Una guarda lo que emitimos por cuenta de "
     "nuestros clientes y otra lo que nosotros les vendemos. Si se mezclaran, el tablero "
     "contaría como ingreso propio los documentos de terceros.", "Johan"),
    ("¿Qué pasa si se cae el correo del comprador?",
     "La factura ya quedó emitida y es válida. El envío se hace después de responder y fuera "
     "de la transacción, y el resultado queda anotado en la bitácora del documento. Un "
     "servidor de correo caído no puede impedir que una empresa facture.", "Johan"),
    ("¿Cuántas empresas encuestaron y cómo las eligieron?",
     "Cuarenta y cinco empresas de Cúcuta, de comercio al detal, servicios profesionales y "
     "salud, seleccionadas por conveniencia entre negocios con establecimiento abierto al "
     "público. Lo declaramos como limitación en el documento, porque sirve para orientar el "
     "diseño y no como estimación estadística del país.", "Wilmer"),
    ("¿Qué pasa si un cliente se pasa del cupo de su plan?",
     "Si es una factura, se rechaza antes de tomar un número, con un código de error "
     "específico. Si es una nota crédito o débito, se permite igual, porque negarle a un "
     "cliente corregir una factura mal emitida lo dejaría con un documento equivocado ante "
     "la DIAN y sin forma de arreglarlo hasta el mes siguiente.", "Wilmer"),
    ("¿Usaron inteligencia artificial en el proyecto?",
     "Sí, como herramienta de apoyo, y está declarado en las tecnologías. La usamos para "
     "revisar código, contrastar decisiones de diseño y redactar documentación. Las "
     "decisiones de arquitectura y el análisis son nuestros, y podemos sustentar cada una.",
     "Johan"),
    ("¿Cómo se cobra el servicio?",
     "Por suscripción mensual según el volumen de documentos. Hay tres planes y los "
     "documentos que exceden el cupo se cobran aparte. El consumo se cuenta de los "
     "documentos realmente emitidos, no de un contador guardado, para que lo que el sistema "
     "muestra y lo que se factura no puedan separarse.", "Brandon"),
]


def construir():
    d = DocumentoAPA()
    for nombre in ("Normal", "Heading 1", "Heading 2", "Heading 3"):
        d.doc.styles[nombre].paragraph_format.line_spacing = 1.15
    # Con interlineado sencillo los títulos quedan pegados al párrafo anterior y la
    # hoja se lee como un bloque único.
    for nombre in ("Heading 1", "Heading 2", "Heading 3"):
        d.doc.styles[nombre].paragraph_format.space_before = Pt(14)
        d.doc.styles[nombre].paragraph_format.space_after = Pt(4)

    d.portada(
        titulo="FACTUGEST",
        subtitulo="Guion de la sustentación",
        integrantes=["Brandon Arley Restrepo Gélvez",
                     "Johan Sebastián Acosta Sánchez",
                     "Wilmer Jesús Contreras Rangel"],
        grado="Ficha 3115426\nTecnólogo en Análisis y Desarrollo de Software",
        institucion=["SERVICIO NACIONAL DE APRENDIZAJE (SENA)",
                     "Centro de la Industria, la Empresa y los Servicios (CIES)"],
        ciudad="CÚCUTA, NORTE DE SANTANDER",
        anio=2026,
    )

    _como_usarla(d)
    _reparto(d)
    _antes(d)
    _guion(d, "Brandon Arley Restrepo Gélvez", "Formulación del proyecto", BRANDON)
    _guion(d, "Wilmer Jesús Contreras Rangel", "Análisis y diseño", WILMER)
    _guion(d, "Johan Sebastián Acosta Sánchez", "Metodología, desarrollo e implementación",
           JOHAN)
    _preguntas(d)
    _ensayo(d)
    _compactar(d)

    SALIDA.mkdir(parents=True, exist_ok=True)
    d.guardar(ARCHIVO)
    return d


def _compactar(d):
    """Interlineado sencillo en todo el documento.

    `vinetas()` y `numerada()` fijan el interlineado doble del instructivo, que aquí
    estorba: esto se lee de reojo mientras se habla, no se entrega a un jurado.
    """
    for parrafo in d.doc.paragraphs:
        parrafo.paragraph_format.line_spacing = 1.15


def _como_usarla(d):
    d.titulo("Cómo usar esta guía", nivel=1)
    d.parrafo(
        "Cada diapositiva trae dos cosas, lo que el jurado ve en pantalla y lo que conviene "
        "decir mientras la ve. El texto de «qué decir» está escrito para hablarse, no para "
        "leerse en voz alta. Léanlo varias veces hasta que sea suyo y después díganlo con "
        "sus palabras.", interlineado=1.15)
    d.parrafo(
        "Las diapositivas no se leen. Todo lo que está proyectado el jurado ya lo puede leer "
        "solo, así que quien expone aporta lo que no está escrito, que es el porqué de cada "
        "decisión.", interlineado=1.15)
    d.parrafo(
        "Al final hay diez preguntas probables con su respuesta y con el nombre de quién "
        "debería contestarlas. Conviene que las tres personas las conozcan, porque el jurado "
        "pregunta a quien quiera.", interlineado=1.15)


def _reparto(d):
    d.titulo("Reparto de la exposición", nivel=1)
    d.tabla(
        "Quién expone cada parte",
        ["Expositor", "Rol en el proyecto", "Diapositivas", "Contenido", "Tiempo"],
        [[n, rol, diapositivas, contenido, tiempo]
         for n, rol, diapositivas, contenido, tiempo in REPARTO],
        nota="El reparto sigue los roles declarados en el capítulo 3 del documento. Cada uno "
             "expone lo que le tocó construir, de modo que si el jurado pregunta, responde "
             "quien lo hizo.",
        anchos=[3.8, 2.2, 2.6, 5.3, 2.1],
    )
    d.parrafo(
        "El total son treinta minutos de exposición. Si les dan menos tiempo, lo primero que "
        "se recorta son las diapositivas 13, 16 y 17, que son historias de usuario y "
        "requisitos relacionados, y se pueden resumir en una frase cada bloque. Lo que no se "
        "puede recortar es la diapositiva 12, que es donde está el hallazgo, ni la 37, que es "
        "la evidencia de que el sistema funciona.", interlineado=1.15)


def _antes(d):
    d.titulo("Antes de empezar", nivel=1)
    d.vinetas([
        "Abran la presentación desde el archivo, no desde el PDF, para que las transiciones "
        "y la numeración funcionen.",
        "Tengan el documento de grado impreso o abierto a mano. Si preguntan por un dato, es "
        "más sólido mostrarlo que recordarlo.",
        "Si van a hacer la demostración en vivo con el punto de venta, prepárenla antes y "
        "tengan un video de respaldo por si falla la conexión.",
        "Repártanse quién maneja el computador. Quien expone no debería estar pasando "
        "diapositivas.",
        "Hablen de «nosotros» cuando se refieran al proyecto y de «yo» cuando se refieran a "
        "lo que cada uno hizo.",
    ])


def _guion(d, expositor, parte, diapositivas):
    partes = expositor.split()
    d.titulo(f"Guion de {partes[0]} {partes[2]}", nivel=1, nueva_pagina=True)
    d.parrafo(f"{parte}. Diapositivas {diapositivas[0][0]} a {diapositivas[-1][0]}.",
              sangria=False, cursiva=True, interlineado=1.15)
    d.parrafo()
    for numero, titulo, pantalla, texto in diapositivas:
        d.titulo(f"Diapositiva {numero}. {titulo}", nivel=3)
        p = d.parrafo(sangria=False, interlineado=1.15)
        p.add_run("En pantalla. ").bold = True
        p.add_run(pantalla)
        p = d.parrafo(sangria=False, interlineado=1.15)
        p.add_run("Qué decir. ").bold = True
        p.add_run(texto)
        d.parrafo()


def _preguntas(d):
    d.titulo("Preguntas probables del jurado", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Estas son las preguntas que más probablemente van a hacer, con una respuesta "
        "preparada. La columna de la derecha sugiere quién debería responder, pero si "
        "preguntan a otro, que responda igual y luego el responsable complementa.",
        interlineado=1.15)
    d.tabla(
        "Preguntas frecuentes y respuestas preparadas",
        ["Pregunta", "Respuesta", "Responde"],
        [[pregunta, respuesta, quien] for pregunta, respuesta, quien in PREGUNTAS],
        nota="Elaboración propia.",
        anchos=[4.2, 9.9, 1.9],
    )
    d.parrafo(
        "Si preguntan algo que no saben, la respuesta es decirlo. «No lo verificamos» o «eso "
        "quedó fuera del alcance y está declarado en el documento» son respuestas válidas y "
        "mucho mejores que inventar una cifra.", interlineado=1.15)


def _ensayo(d):
    d.titulo("Lista de verificación para el ensayo", nivel=1, nueva_pagina=True)
    d.numerada([
        "Cronometrar cada bloque por separado. Si alguno se pasa de su tiempo, recortar del "
        "guion, no hablar más rápido.",
        "Ensayar los tres empalmes, que son las diapositivas 10, 25 y 41. Un cambio de "
        "expositor que se nota es lo que más desordena una sustentación.",
        "Repasar en voz alta las cifras que se dicen, o sea 45 empresas, 82 %, 84 %, 82 "
        "requisitos, 56 casos de uso, 27 tablas y 190 pruebas. Son las que el jurado puede contrastar "
        "con el documento.",
        "Comprobar que las tres personas puedan explicar por qué el cupo se valida antes de "
        "reservar el consecutivo. Es la pregunta técnica más probable.",
        "Preparar en una frase la respuesta a por qué el proyecto cambió de alcance a mitad "
        "del desarrollo. Está en el documento y conviene contarlo antes de que lo pregunten.",
        "Revisar que el computador proyecte en 16:9 y que los colores del tablero se vean, "
        "porque en un proyector claro el azul del panel pierde contraste.",
    ])


if __name__ == "__main__":
    documento = construir()
    total = len(BRANDON) + len(WILMER) + len(JOHAN)
    print(f"Generado: {ARCHIVO}")
    print(f"Diapositivas cubiertas: {total} · Preguntas preparadas: {len(PREGUNTAS)}")
