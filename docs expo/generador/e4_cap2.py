"""
E4 — Capítulo 2. Marco referencial del proyecto.

Este es el capítulo que **cita**, y de sus citas sale la lista de referencias de
T15. Las fuentes son todas verificables y se citan por parafraseo, sin número de
página: no se transcribe texto de ninguna de ellas.

Las referencias declaradas aquí viven en `FUENTES`, y `e4_cierre.py` construirá la
lista bibliográfica a partir de esa misma estructura. Escribir las referencias
aparte llevaría a lo de siempre: una fuente citada en el cuerpo que no aparece en
la lista, o una lista con fuentes que nadie citó.
"""

# (clave, cita en el texto, referencia completa en APA 7)
FUENTES = {
    "et616": ("Estatuto Tributario, art. 616-1",
              "Estatuto Tributario Nacional [ETN]. Art. 616-1. Factura o documento "
              "equivalente. Decreto 624 de 1989 (Colombia)."),
    "dian42": ("DIAN, 2020",
               "Dirección de Impuestos y Aduanas Nacionales. (2020). Resolución 000042 de "
               "2020: por la cual se desarrollan los sistemas de facturación, los proveedores "
               "tecnológicos y se expide el anexo técnico de factura electrónica de venta. "
               "DIAN."),
    "ubl": ("OASIS, 2013",
            "Organization for the Advancement of Structured Information Standards. (2013). "
            "Universal Business Language Version 2.1: OASIS Standard. OASIS."),
    "fielding": ("Fielding, 2000",
                 "Fielding, R. T. (2000). Architectural styles and the design of "
                 "network-based software architectures [Tesis doctoral, University of "
                 "California, Irvine]."),
    "richardson": ("Richardson y Ruby, 2007",
                   "Richardson, L., y Ruby, S. (2007). RESTful web services. O'Reilly "
                   "Media."),
    "openapi": ("OpenAPI Initiative, 2021",
                "OpenAPI Initiative. (2021). OpenAPI Specification v3.1.0. The Linux "
                "Foundation."),
    "codd": ("Codd, 1970",
             "Codd, E. F. (1970). A relational model of data for large shared data banks. "
             "Communications of the ACM, 13(6), 377-387."),
    "sommerville": ("Sommerville, 2011",
                    "Sommerville, I. (2011). Ingeniería de software (9.ª ed.). Pearson "
                    "Educación."),
    "pressman": ("Pressman y Maxim, 2020",
                 "Pressman, R. S., y Maxim, B. R. (2020). Ingeniería del software: un "
                 "enfoque práctico (9.ª ed.). McGraw-Hill."),
    "iso25010": ("ISO/IEC, 2011",
                 "International Organization for Standardization. (2011). ISO/IEC "
                 "25010:2011. Systems and software engineering. Systems and software "
                 "Quality Requirements and Evaluation (SQuaRE). System and software "
                 "quality models. ISO."),
    "sandhu": ("Sandhu et al., 1996",
               "Sandhu, R. S., Coyne, E. J., Feinstein, H. L., y Youman, C. E. (1996). "
               "Role-based access control models. Computer, 29(2), 38-47."),
    "provos": ("Provos y Mazières, 1999",
               "Provos, N., y Mazières, D. (1999). A future-adaptable password scheme. "
               "Proceedings of the USENIX Annual Technical Conference, 81-91."),
    "scrum": ("Schwaber y Sutherland, 2020",
              "Schwaber, K., y Sutherland, J. (2020). La Guía de Scrum: la guía definitiva "
              "de Scrum, las reglas del juego. Scrum.org."),
}


def cita(clave):
    return FUENTES[clave][0]


CONCEPTUAL = [
    ("Factura electrónica de venta",
     "documento que soporta una operación de venta de bienes o servicios, generado y "
     "transmitido en formato electrónico conforme a las condiciones que fija la "
     "administración tributaria."),
    ("Nota crédito",
     "documento electrónico que corrige una factura ya expedida disminuyendo su valor, por "
     "devolución, anulación o descuento posterior."),
    ("Nota débito",
     "documento electrónico que corrige una factura ya expedida aumentando su valor, por "
     "intereses, gastos o mayores valores no incluidos."),
    ("CUFE",
     "código único de facturación electrónica. Valor irrepetible que identifica cada "
     "documento y permite verificar que su contenido no fue alterado."),
    ("Resolución de facturación",
     "acto administrativo mediante el cual la autoridad tributaria autoriza a una empresa un "
     "prefijo y un rango de numeración, por un periodo determinado."),
    ("Consecutivo",
     "número que ocupa un documento dentro del rango autorizado. No puede repetirse ni "
     "saltarse arbitrariamente."),
    ("Emisor",
     "empresa por cuenta de la cual se expide el documento y cuya identificación aparece en "
     "él."),
    ("Adquiriente o comprador",
     "persona natural o jurídica que recibe el bien o el servicio y a quien va dirigido el "
     "documento."),
    ("Proveedor tecnológico",
     "persona jurídica que presta a otras empresas los servicios de generación, transmisión "
     "y entrega de documentos electrónicos."),
    ("Middleware",
     "componente que se sitúa entre dos sistemas y les permite comunicarse sin que ninguno de "
     "los dos tenga que modificar su funcionamiento interno."),
    ("API",
     "interfaz de programación de aplicaciones. Conjunto de operaciones que un sistema expone "
     "para que otro sistema las consuma."),
    ("Llave de API",
     "credencial con la que un sistema externo se identifica ante otro. Sustituye al usuario "
     "y la contraseña cuando quien se autentica es un programa y no una persona."),
    ("Idempotencia",
     "propiedad por la cual repetir una operación produce el mismo resultado que ejecutarla "
     "una sola vez. Es lo que permite reintentar una petición sin duplicar el documento."),
    ("Plan de suscripción",
     "modalidad de contratación en la que el cliente paga una tarifa periódica que incluye "
     "una cantidad determinada de documentos."),
    ("Cupo",
     "cantidad de documentos que el plan contratado incluye dentro del mes."),
    ("Excedente",
     "documento emitido por encima del cupo del plan, que se cobra de forma independiente."),
    ("Auditoría",
     "registro de las operaciones realizadas sobre el sistema, con el usuario que las hizo y "
     "el momento en que ocurrieron."),
    ("Trazabilidad",
     "posibilidad de reconstruir la historia de un dato o de un documento a partir de los "
     "registros que el sistema conserva."),
    ("Rol",
     "conjunto de permisos que determina a qué funciones y a qué información puede acceder un "
     "usuario."),
    ("Tablero de control",
     "pantalla que reúne los indicadores de la operación y los presenta de forma gráfica para "
     "apoyar la toma de decisiones."),
]

TECNOLOGICO = [
    ("Arquitectura cliente-servidor",
     "modelo en el que un servidor centraliza el procesamiento y el almacenamiento, y los "
     "clientes, sean navegadores o sistemas externos, consumen sus servicios por la red."),
    ("Python",
     "lenguaje de programación empleado para construir la totalidad del lado del servidor. Se "
     "eligió por su legibilidad y por la madurez de sus bibliotecas para generación de "
     "documentos y acceso a datos."),
    ("FastAPI",
     "framework web sobre el que se construyeron tanto las rutas de la aplicación como la API "
     "de integración. Valida los datos de entrada a partir de tipos declarados y publica de "
     "forma automática el contrato de la interfaz, lo que reduce el esfuerzo de quien "
     "integra."),
    ("Uvicorn",
     "servidor de aplicación que ejecuta el proyecto y atiende las peticiones HTTP."),
    ("Pydantic",
     "biblioteca de validación con la que se declaran los modelos de entrada y salida de la "
     "API. Un dato que no cumple el modelo no llega a la lógica de negocio."),
    ("Jinja2",
     "motor de plantillas con el que se generan las páginas de la aplicación web a partir de "
     "los datos que entrega el servidor."),
    ("Bootstrap",
     "biblioteca de estilos utilizada para la interfaz del panel, que le da un comportamiento "
     "adaptable a distintos tamaños de pantalla."),
    ("Chart.js",
     "biblioteca de gráficas empleada en el tablero de control para presentar las series de "
     "documentos emitidos y de facturación."),
    ("MySQL",
     "sistema gestor de base de datos relacional donde reside toda la información del "
     "sistema. Se accede mediante consultas SQL explícitas, sin mapeador objeto-relacional, "
     "para conservar el control sobre cada consulta."),
    ("ReportLab",
     "biblioteca con la que se construye la representación gráfica en PDF de cada documento "
     "emitido."),
    ("bcrypt",
     "algoritmo de derivación con el que se calcula el hash de las contraseñas. Su costo es "
     "ajustable, de modo que puede endurecerse a medida que el hardware avanza."),
    ("OpenAPI y Swagger",
     "especificación e interfaz con las que el contrato de la API queda publicado y "
     "explorable, generadas a partir del propio código."),
    ("Git y GitHub",
     "sistema de control de versiones y plataforma de alojamiento remoto empleados para "
     "gestionar los cambios del código y el trabajo colaborativo."),
    ("PyCharm",
     "entorno de desarrollo utilizado para la escritura, depuración y mantenimiento del "
     "código fuente."),
    ("pytest",
     "herramienta con la que se ejecutan las pruebas automatizadas sobre la aritmética "
     "tributaria, el contrato de la API y la generación de documentos."),
]


def escribir(d):
    d.titulo("Capítulo 2. Marco referencial del proyecto", nivel=1, nueva_pagina=True)
    _teorico(d)
    _conceptual(d)
    _tecnologico(d)


def _concepto(d, termino, texto):
    p = d.parrafo()
    p.add_run(f"{termino}. ").bold = True
    p.add_run(texto)
    return p


def _teorico(d):
    d.titulo("2.1 Marco teórico", nivel=2)
    d.parrafo(
        "El marco teórico reúne los fundamentos sobre los que se sostiene la solución "
        "propuesta, esto es, la naturaleza de la facturación electrónica como sistema de "
        "información "
        "con efectos jurídicos, el modelo de intermediación que permite integrarla sin "
        "reemplazar el software existente, los estilos de arquitectura empleados y los "
        "principios de seguridad y de calidad que rigen su construcción."
    )

    _concepto(d, "La facturación electrónica como sistema de información tributario",
              "La factura electrónica no es la versión digital de un documento impreso. Es un "
              "documento con validez jurídica cuya estructura, numeración y contenido están "
              f"determinados por la norma ({cita('et616')}). La reglamentación colombiana "
              "establece las condiciones de generación, transmisión y entrega de estos "
              "documentos, así como la figura del proveedor tecnológico, habilitado para "
              f"prestar esos servicios a otras empresas ({cita('dian42')}). De esta "
              "naturaleza normativa se desprende una consecuencia técnica que atraviesa todo "
              "el proyecto. Los errores no degradan el servicio, lo invalidan. Un consecutivo "
              "repetido o un archivo que no cumple el estándar no producen un documento "
              "defectuoso, producen un documento rechazado.")

    _concepto(d, "Estándares de documentos comerciales electrónicos",
              "Para que un documento pueda ser procesado automáticamente por sistemas "
              "distintos, su contenido debe expresarse en una estructura común. El estándar "
              "Universal Business Language define, en formato XML, la representación de los "
              "documentos comerciales, entre ellos la factura, la nota crédito y la nota "
              f"débito, y es el adoptado por la normativa colombiana ({cita('ubl')}). "
              "Trabajar sobre un estándar y no sobre un formato propio es lo que permite que "
              "un documento emitido por una plataforma sea legible por la autoridad "
              "tributaria y por el sistema del comprador sin acuerdos previos entre ellos.")

    _concepto(d, "Arquitectura orientada a servicios y el modelo de middleware",
              "Un middleware es un componente que se ubica entre dos sistemas y les permite "
              "comunicarse sin que ninguno modifique su funcionamiento interno. Aplicado a "
              "este proyecto, significa que la empresa conserva el software con el que opera "
              "y que la plataforma se encarga únicamente de convertir los datos de una venta "
              "en un documento electrónico válido. La integración se resuelve mediante "
              "servicios expuestos por la red, un enfoque que permite que sistemas "
              "construidos con tecnologías distintas colaboren a través de contratos "
              f"explícitos ({cita('sommerville')}).")

    _concepto(d, "El estilo arquitectónico REST",
              "REST es un estilo de arquitectura para sistemas distribuidos que organiza la "
              "interacción alrededor de recursos identificados por una dirección, sobre los "
              "que se actúa con un conjunto reducido de operaciones y en el que cada petición "
              f"contiene por sí sola la información necesaria para ser atendida "
              f"({cita('fielding')}). Esa última propiedad, la de que el servidor no conserve "
              "estado de conversación entre peticiones, es la que hace que una interfaz de "
              "este tipo pueda ser consumida por un punto de venta, por un sistema contable o "
              f"por una aplicación móvil sin distinción ({cita('richardson')}). El contrato "
              "de la interfaz puede además describirse en un formato legible por máquinas, lo "
              "que permite generar documentación y clientes de forma automática a partir de "
              f"la misma definición ({cita('openapi')}).")

    _concepto(d, "Arquitectura por capas y separación de responsabilidades",
              "La organización del software en capas con responsabilidades separadas, que son "
              "presentación, lógica de negocio y acceso a datos, permite que un cambio en una "
              f"de ellas no obligue a modificar las demás ({cita('pressman')}). En este "
              "proyecto la separación cumple además una función concreta, ya que la misma lógica de "
              "negocio alimenta la aplicación web y la interfaz de integración, de modo que "
              "una regla tributaria se implementa una sola vez y rige por igual para las dos. "
              "Duplicarla habría producido, tarde o temprano, dos resultados distintos para "
              "la misma operación.")

    _concepto(d, "El modelo relacional de datos",
              "El modelo relacional organiza la información en relaciones compuestas por "
              "atributos, e independiza la forma en que los datos se consultan de la forma en "
              f"que se almacenan ({cita('codd')}). Sus mecanismos de integridad, como las claves "
              "primarias, las claves foráneas y las restricciones de unicidad, no son una formalidad "
              "de diseño en un sistema como este, sino lo que impide que dos documentos del "
              "mismo emisor compartan número o que una línea quede huérfana de su documento.")

    _concepto(d, "Seguridad, autenticación y control de acceso",
              "La protección de un sistema de información se apoya en dos mecanismos "
              "distintos. La autenticación establece quién realiza una petición; el control "
              "de acceso determina qué puede hacer una vez identificado. El control de acceso "
              "basado en roles asigna los permisos a roles y no a personas, de modo que "
              "administrar el acceso de un usuario se reduce a asignarle el rol que "
              f"corresponde ({cita('sandhu')}). Respecto de las contraseñas, la práctica "
              "aceptada es no almacenarlas y guardar en su lugar el resultado de una función de "
              "derivación de costo ajustable, que puede endurecerse con el tiempo sin "
              f"cambiar el esquema ({cita('provos')}).")

    _concepto(d, "Calidad del software",
              "La calidad de un producto de software puede describirse mediante "
              "características medibles, como la adecuación funcional, la eficiencia, la "
              "compatibilidad, la "
              "usabilidad, la fiabilidad, la seguridad, la mantenibilidad y la portabilidad, que sirven "
              f"tanto para especificar como para evaluar ({cita('iso25010')}). Los requisitos "
              "no funcionales de este proyecto se organizaron siguiendo esa lógica, y cada "
              "uno se acompaña de la forma en que se comprueba, porque un atributo de calidad que no "
              "indica cómo verificarse no puede declararse cumplido.")

    _concepto(d, "Modelos de negocio basados en suscripción",
              "En el modelo de software como servicio, el cliente no adquiere una licencia "
              "sino el derecho a usar un servicio durante un periodo, y el proveedor conserva "
              "la responsabilidad de operarlo. Cuando la tarifa se asocia al volumen "
              "consumido, el costo de entrada disminuye y se vuelve proporcional al tamaño "
              "del negocio, lo que resulta determinante para una empresa pequeña, que paga por "
              "los documentos que emite y no por una licencia dimensionada para volúmenes que "
              "no maneja.")


def _conceptual(d):
    d.titulo("2.2 Marco conceptual", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Se relacionan a continuación los términos empleados a lo largo del documento, con el "
        "significado preciso que tienen dentro del dominio de la facturación electrónica y de "
        "este proyecto en particular."
    )
    d.vinetas(CONCEPTUAL)


def _tecnologico(d):
    d.titulo("2.3 Marco tecnológico", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Se describen las tecnologías empleadas en la construcción de la solución, indicando "
        "la función que cumple cada una dentro del sistema."
    )
    d.vinetas(TECNOLOGICO)
