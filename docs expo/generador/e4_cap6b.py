"""
E4 — Capítulo 6, parte B. Integración, pruebas, resultados y tecnologías.

Las cifras de las pruebas automatizadas son reales y se obtuvieron ejecutando la
batería del proyecto. Si vuelven a correrse y el número cambia, hay que actualizar
`PRUEBAS_AUTOMATICAS`, porque un documento que declara ciento noventa pruebas
mientras el proyecto tiene otras tantas deja de servir como evidencia.

    cd Factugest/Factugest && python -m pytest
"""
from pathlib import Path

CAPTURAS = Path(__file__).resolve().parent.parent / "documento para que te guies claude"

PRUEBAS_AUTOMATICAS = 190
SEGUNDOS = "3,3"
ARCHIVOS_PRUEBA = 12

COBERTURA = [
    ("Aritmética tributaria", "test_calculo_documento, test_calculo_notas",
     "Bases gravables, descuentos de línea y de documento, prorrateo de IVA y totales, "
     "tanto en facturas como en notas."),
    ("Contrato de la API", "test_modelos_api, test_validaciones",
     "Validación de los datos de entrada y forma de la respuesta y de los errores."),
    ("Documento canónico", "test_documento_canonico",
     "Estructura que comparten la generación del PDF y la del XML."),
    ("Generación del XML", "test_xml_service",
     "Puntos del archivo UBL 2.1 donde el emisor cambia la salida."),
    ("Generación del PDF", "test_pdf_membrete, test_pdf_descuentos, test_monograma",
     "Membrete con la identidad del emisor, filas de descuentos con su porcentaje correcto "
     "y monograma de la empresa sin logo."),
    ("Llaves de acceso", "test_api_key_service",
     "Generación, verificación, rotación y cambio de estado de las llaves."),
    ("Consumo del plan", "test_consumo_service",
     "Conteo del consumo, periodo facturable y cálculo de excedentes."),
    ("Proveedor de emisión", "test_dian_proveedor",
     "Comportamiento ante las respuestas del proveedor de transmisión."),
]

EVIDENCIAS = [
    ("RF 4.3", "Registro de un servicio",
     "Registro de servicios.png", "registro de servicios emitidos.png",
     "Se diligencia el formulario de creación de un servicio del catálogo, indicando su "
     "código, nombre, descripción, precio, unidad e impuesto aplicable.",
     "El servicio queda registrado y aparece en el catálogo, disponible para ser incluido en "
     "una factura."),
    ("RF 4.2", "Registro de un cliente",
     "registro de nuevo cliente.png", "registro de nuevo cliente emitido.png",
     "Se diligencia el formulario de creación de un cliente con su tipo y número de "
     "documento, razón social, correo, teléfono y ubicación.",
     "El cliente queda registrado y disponible para facturarle, y la operación queda anotada "
     "en el registro de auditoría."),
    ("RF 4.1", "Emisión de una factura",
     "registro de nueva factura.png", "registro de nueva factura emitida.png",
     "Se selecciona el cliente, se agregan las líneas del servicio facturado, se indica la "
     "forma de pago y se confirma la emisión.",
     "La factura queda emitida con su número consecutivo y su código único, con los totales "
     "calculados, y su representación gráfica queda disponible para descarga."),
    ("RF 7.7", "Creación de un usuario",
     "registro de nuevo usuario.png", "registro de nuevo usuario emitido.png",
     "Se diligencia el formulario de creación de usuario con su nombre, credenciales, rol y "
     "empresa asignada.",
     "El usuario queda creado con su contraseña almacenada como hash y con el alcance que su "
     "rol determina."),
]

RESULTADOS = [
    ("Emisión de documentos electrónicos",
     "Facturas de venta, notas crédito y notas débito con consecutivo autorizado, código "
     "único, representación gráfica y archivo XML bajo el estándar UBL 2.1.", "Cumplido"),
    ("Interfaz de integración",
     "Nueve operaciones disponibles, autenticadas por llave individual, con forma única de "
     "error y contrato publicado de forma automática.", "Cumplido"),
    ("Control de cupo y suscripción",
     "Consumo calculado sobre los documentos emitidos, bloqueo por cupo agotado y "
     "facturación de la mensualidad con sus excedentes.", "Cumplido"),
    ("Tablero de control y reportes",
     "Indicadores del servicio y de la venta con filtro de periodo, y siete reportes "
     "exportables a CSV y a PDF.", "Cumplido"),
    ("Seguridad y auditoría",
     "Autenticación con contraseñas cifradas, cuatro roles con control de acceso por ruta, "
     "cierre de sesión por inactividad y registro de las operaciones de escritura.",
     "Cumplido"),
    ("Transmisión en producción ante la DIAN",
     "El código único se genera en modalidad de pruebas, a la espera de la habilitación del "
     "proveedor.", "Parcial"),
]

TECNOLOGIAS = [
    ("Python", "3.13", "Lenguaje del lado del servidor"),
    ("FastAPI", "0.135.1", "Framework de las rutas web y de la interfaz de integración"),
    ("Uvicorn", "0.41.0", "Servidor de aplicación que atiende las peticiones"),
    ("Pydantic", "incluido con FastAPI", "Validación de los datos de entrada y salida"),
    ("Jinja2", "3.1.6", "Motor de plantillas de la interfaz web"),
    ("Bootstrap", "5.3.2", "Biblioteca de estilos del panel"),
    ("Chart.js", "4.x", "Gráficas del tablero de control"),
    ("MySQL", "8.0", "Gestor de base de datos relacional"),
    ("mysql-connector-python", "9.5.0", "Conector de acceso a la base de datos"),
    ("ReportLab", "4.2.5", "Generación de la representación gráfica en PDF"),
    ("bcrypt", "4.2.1", "Cifrado de las contraseñas de los usuarios"),
    ("itsdangerous", "2.2.0", "Firma de las cookies de sesión"),
    ("httpx", "0.28.1", "Cliente con el que el sistema consume su propia interfaz"),
    ("Pillow", "10.0 o superior", "Validación y normalización de las fotos de perfil"),
    ("num2words", "0.5.14", "Conversión del total a letras en la representación gráfica"),
    ("qrcode", "8.0", "Código de respuesta rápida del documento"),
    ("pytest", "8.x", "Ejecución de las pruebas automatizadas"),
    ("Git y GitHub", "No aplica", "Control de versiones y trabajo colaborativo"),
    ("PyCharm", "2025", "Entorno de desarrollo"),
]


def escribir(d):
    _integracion(d)
    _pruebas(d)
    _evidencias(d)
    _resultados(d)
    _analisis(d)
    _tecnologias(d)


def _integracion(d):
    d.titulo("6.5 Integración de módulos", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Los módulos no funcionan de manera aislada, sino que se apoyan unos en otros a "
        "través de la capa de servicios. La integración se resolvió haciendo que cada módulo "
        "exponga su lógica como un servicio que los demás invocan, en lugar de que cada uno "
        "consulte directamente las tablas del otro."
    )
    d.parrafo(
        "La emisión de la mensualidad es el caso donde esa integración se ve con más "
        "claridad, porque atraviesa cuatro módulos. El de consumo determina el periodo "
        "facturable y cuenta los documentos emitidos; el de planes y servicios aporta la "
        "tarifa y el valor del documento excedente; el de integración expide el documento "
        "electrónico; y el de facturación propia guarda la factura con el número y el código "
        "único que la interfaz devolvió."
    )
    d.parrafo(
        "Ese recorrido tiene una particularidad que conviene señalar, y es que el sistema "
        "consume su propia interfaz de integración para facturarse. La alternativa habría "
        "sido escribir un segundo camino de emisión para uso interno, con lo cual existirían "
        "dos maneras de expedir un documento y solo una estaría probada por los clientes "
        "todos los días. Al usar la misma, cualquier fallo en la emisión aparece primero en "
        "la propia facturación del proveedor."
    )
    d.parrafo(
        "La segunda integración relevante es la del módulo de documentos con el de consumo. "
        "Antes de emitir una factura, la interfaz consulta el cupo disponible del cliente, y "
        "ese dato no proviene de un contador almacenado sino del conteo de los documentos "
        "efectivamente emitidos. De esa forma el módulo de consumo no necesita que nadie le "
        "avise cuando se emite un documento, porque lee la misma fuente."
    )
    d.parrafo(
        "El registro de auditoría integra a todos los módulos de escritura, y lo hace bajo "
        "una condición estricta, ya que un fallo al anotar no puede interrumpir la operación "
        "auditada. Un sistema que deja de facturar porque no pudo registrar que facturó es "
        "peor que uno sin auditoría."
    )


def _pruebas(d):
    d.titulo("6.6 Pruebas", nivel=2, nueva_pagina=True)

    d.titulo("6.6.1 Objetivos de las pruebas", nivel=3)
    d.parrafo(
        "Las pruebas se orientaron a comprobar que el sistema cumple lo especificado y que se "
        "comporta correctamente cuando algo sale mal. En un sistema que expide documentos con "
        "efectos tributarios el segundo objetivo pesa tanto como el primero, porque un fallo "
        "mal atendido no produce una molestia sino un documento inválido o un consecutivo "
        "gastado."
    )
    d.vinetas([
        "Verificar que cada requisito funcional produce el resultado especificado.",
        "Comprobar que la aritmética tributaria arroja los mismos valores en la aplicación "
        "web y en la interfaz de integración.",
        "Confirmar que un fallo a mitad de una emisión no deja rastro parcial ni consume un "
        "número de la resolución.",
        "Verificar que los documentos generados conservan la identidad de la empresa emisora "
        "y no la del proveedor.",
        "Comprobar que el control de acceso impide a cada rol lo que no le corresponde.",
        "Confirmar que la indisponibilidad de un servicio externo no impide emitir.",
    ])

    d.titulo("6.6.2 Alcance de las pruebas", nivel=3)
    d.parrafo(
        "Se aplicaron pruebas funcionales sobre la interfaz, ejecutadas manualmente siguiendo "
        "los casos de uso documentados, y pruebas automatizadas sobre la lógica de negocio, "
        "que se ejecutan en cada cambio del código."
    )
    d.parrafo(
        f"La batería automatizada comprende {PRUEBAS_AUTOMATICAS} pruebas repartidas en "
        f"{ARCHIVOS_PRUEBA} archivos, que se ejecutan en {SEGUNDOS} segundos y actualmente "
        "pasan en su totalidad. Se concentran en lo que no requiere base de datos y en lo que "
        "resultaría costoso verificar a mano, es decir, el cálculo de impuestos con sus "
        "descuentos y su prorrateo, el contrato de la interfaz y los puntos de la generación "
        "de documentos donde el emisor cambia la salida."
    )
    d.tabla(
        "Cobertura de las pruebas automatizadas",
        ["Área", "Archivos", "Qué comprueba"],
        [[area, archivos, que] for area, archivos, que in COBERTURA],
        nota=f"Elaboración propia. En total {PRUEBAS_AUTOMATICAS} pruebas, ejecutadas con "
             "pytest.",
        anchos=[3.5, 4.4, 8.4],
    )
    d.parrafo(
        "Quedó fuera del alcance la prueba de carga sostenida, ya que verificar el "
        "comportamiento del sistema con un número elevado de emisiones simultáneas exige una "
        "infraestructura de producción de la que el proyecto no dispuso. También quedó fuera "
        "la validación del documento contra los servicios en producción de la administración "
        "tributaria, que depende de la habilitación del proveedor."
    )


def _evidencias(d):
    d.titulo("6.7 Evidencia de pruebas", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Se documentan a continuación cuatro pruebas funcionales representativas. De cada una "
        "se presenta el formulario diligenciado y el resultado obtenido, de modo que pueda "
        "compararse lo que se ingresó con lo que el sistema produjo."
    )
    for indice, (rf, nombre, antes, despues, entrada, esperado) in enumerate(EVIDENCIAS,
                                                                            start=1):
        d.titulo(f"6.7.{indice} {rf}. {nombre}", nivel=3, nueva_pagina=(indice > 1))
        d.tabla(
            f"Caso de prueba {indice}. {nombre}",
            ["Aspecto", "Descripción"],
            [
                ["Requisito verificado", rf],
                ["Objetivo", f"Comprobar que el sistema permite realizar el "
                             f"{nombre.lower()} y que el registro queda disponible."],
                ["Datos de entrada", entrada],
                ["Resultado esperado", esperado],
                ["Resultado obtenido", "Coincide con el resultado esperado."],
                ["Estado", "Satisfactorio"],
            ],
            nota="Elaboración propia.",
            anchos=[4.0, 12.3],
        )
        d.figura(
            f"{nombre}. Formulario diligenciado",
            CAPTURAS / antes,
            nota="Elaboración propia. Datos ingresados antes de confirmar la operación.",
        )
        d.figura(
            f"{nombre}. Resultado obtenido",
            CAPTURAS / despues,
            nota="Elaboración propia. Estado del sistema después de confirmar la operación.",
        )


def _resultados(d):
    d.titulo("6.8 Resultados obtenidos", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El proyecto entregó una plataforma en funcionamiento que cumple los objetivos "
        "específicos planteados en el capítulo 1. Se resume a continuación el estado de cada "
        "uno frente a lo que se propuso."
    )
    d.tabla(
        "Estado de cumplimiento de los objetivos",
        ["Objetivo", "Resultado alcanzado", "Estado"],
        [[objetivo, resultado, estado] for objetivo, resultado, estado in RESULTADOS],
        nota="Elaboración propia.",
        anchos=[4.0, 9.3, 3.0],
    )
    d.parrafo(
        "Junto con la plataforma se produjeron los artefactos de análisis y diseño que la "
        "sustentan, que comprenden ochenta y dos requisitos funcionales y treinta y dos no "
        "funcionales especificados y priorizados, cincuenta y seis casos de uso con sus nueve "
        "diagramas y su documentación, el modelo de datos con veintisiete tablas y su "
        "diccionario, y una batería de pruebas automatizadas que se ejecuta en segundos."
    )
    d.parrafo(
        "La demostración de que la solución resuelve el problema planteado se realizó "
        "integrando un punto de venta en operación que no emitía facturación electrónica. Ese "
        "sistema consumió la interfaz de la plataforma y quedó emitiendo documentos válidos "
        "sin que se modificara la forma en que registra sus ventas, que es exactamente lo que "
        "el proyecto se propuso demostrar."
    )


def _analisis(d):
    d.titulo("6.9 Análisis de resultados", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Los resultados confirman que la vía elegida responde a la barrera identificada en el "
        "diagnóstico. La encuesta había mostrado que el ochenta y cuatro por ciento de las "
        "empresas consultadas facturaría electrónicamente si no tuviera que cambiar de "
        "software, y la integración del punto de venta demuestra que esa condición puede "
        "cumplirse en la práctica y no solo enunciarse."
    )
    d.parrafo(
        "Tres decisiones técnicas resultaron determinantes y conviene evaluarlas. La primera "
        "fue concentrar la lógica de negocio en una capa de servicios común a las dos "
        "entradas, lo que evitó que el cálculo tributario tuviera dos implementaciones. Las "
        "pruebas automatizadas de esa capa cubren un solo camino, y por eso valen para ambas."
    )
    d.parrafo(
        "La segunda fue reservar el consecutivo en una sola sentencia y dentro de una "
        "transacción. Es una precaución que no se nota mientras el sistema atiende una "
        "petición a la vez, y que se vuelve indispensable en cuanto dos clientes emiten en el "
        "mismo instante, situación en la que una lectura seguida de una actualización "
        "entregaría el mismo número dos veces."
    )
    d.parrafo(
        "La tercera fue calcular el consumo contando los documentos emitidos en lugar de "
        "mantener un contador. Es más costoso en cada consulta, pero elimina por completo la "
        "posibilidad de que la cifra que el sistema muestra difiera de la que se le factura "
        "al cliente."
    )
    d.parrafo(
        "El cambio de alcance ocurrido durante el desarrollo merece una valoración aparte. "
        "Pasar de un sistema de facturación para una empresa a un proveedor que emite por "
        "cuenta de varias supuso rehacer el análisis de actores y agregar módulos completos, "
        "y sin embargo no obligó a desechar lo construido, porque el motor de emisión, el "
        "cálculo tributario y la generación de documentos siguieron siendo válidos. Lo que "
        "cambió fue la manera de ofrecer el servicio y no la manera de expedir un documento."
    )
    d.parrafo(
        "Queda pendiente la transmisión en producción ante la administración tributaria, que "
        "no depende del desarrollo sino de un trámite de habilitación. El sistema está "
        "construido para ese momento, ya que el proveedor de transmisión está aislado detrás "
        "de una capa propia y sustituirlo no obliga a tocar el resto."
    )


def _tecnologias(d):
    d.titulo("6.10 Tecnologías utilizadas", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Se relacionan las tecnologías empleadas en la construcción del sistema, con la "
        "versión utilizada y la función que cumple cada una."
    )
    d.tabla(
        "Tecnologías utilizadas en el desarrollo",
        ["Tecnología", "Versión", "Función en el sistema"],
        [[t, v, f] for t, v, f in TECNOLOGIAS],
        nota="Elaboración propia. Las versiones corresponden a las declaradas en el archivo "
             "de dependencias del proyecto.",
        anchos=[4.4, 3.4, 8.5],
    )
    d.parrafo(
        "La elección de FastAPI merece una justificación, porque de ella dependen dos "
        "características del sistema. La primera es que valida los datos de entrada a partir "
        "de los tipos declarados, de modo que un dato mal formado se rechaza antes de llegar "
        "a la lógica de negocio y el error indica qué campo lo provocó. La segunda es que "
        "publica el contrato de la interfaz de forma automática a partir del propio código, "
        "lo que significa que la documentación no puede desviarse de lo que el sistema hace, "
        "y esa garantía es lo que permite que un integrador construya su cliente sin "
        "depender de un manual escrito aparte."
    )
