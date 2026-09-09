"""
AA1, capítulos 1 y 2. Introducción y marco de calidad del software.

Es el capítulo que cita, y de sus citas sale parte de la lista de referencias. El
contenido sigue el material de formación del SENA, que es lo que la guía pide
revisar, pero no lo transcribe: cada modelo y cada estándar se presenta con lo que
aporta a un proyecto como este, porque la evidencia es de desempeño y lo que se
evalúa es el criterio con el que el equipo eligió, no cuánto alcanzó a copiar.

Las tablas de factores y características se escriben completas a propósito. El
capítulo 3 selecciona sobre ellas, y una selección sobre una lista que el lector no
tiene delante no se puede juzgar.
"""
from fuentes import cita, narrativa

CITADAS = ["sena", "pressman", "vega", "scalone", "estayno", "fillottrani", "gomez",
           "rae", "ieee", "iso9126", "iso25000", "iso25010", "iso15504", "iso12207",
           "iso9001", "cmmi", "portal25000", "polillo", "alfonzo", "dian42"]


def escribir(d):
    _introduccion(d)
    _definiciones(d)
    _clasificacion(d)
    _modelos_producto(d)
    _modelo_proceso(d)
    _estandares_producto(d)
    _estandares_proceso(d)


def _introduccion(d):
    d.titulo("1. Introducción", nivel=1, nueva_pagina=True)
    d.parrafo(
        "El presente informe corresponde a la evidencia AA1-EV01 de la competencia "
        "«Controlar la calidad del servicio de software de acuerdo con los estándares "
        "técnicos», y recoge el análisis de los marcos de calidad aplicables a FactuGest, "
        "el estándar adoptado para el proyecto y el plan de pruebas con el que se validó "
        "su funcionamiento. No es un estudio general sobre calidad de software, sino la "
        "aplicación de esos marcos a un sistema concreto, construido, en funcionamiento y "
        "verificable, de modo que cada afirmación que aquí se hace sobre el software puede "
        "comprobarse en el repositorio del proyecto."
    )
    d.parrafo(
        "FactuGest es una plataforma web de facturación electrónica que opera como "
        "proveedor tecnológico para micro, pequeñas y medianas empresas de Colombia. A "
        "diferencia de un facturador convencional, no reemplaza el software con el que "
        "trabaja la empresa, sino que emite por cuenta de ella a través de una interfaz de "
        "integración que su propio sistema consume, de manera que el negocio cumple con la "
        "obligación tributaria sin cambiar la herramienta que ya usa. La plataforma expide "
        "facturas de venta, notas crédito y notas débito, calcula las bases gravables, los "
        "descuentos y el prorrateo de impuestos, reserva el consecutivo autorizado en la "
        "resolución de facturación, genera el código único de facturación electrónica, la "
        "representación gráfica en formato PDF y el archivo XML bajo el estándar UBL 2.1, "
        "y hace llegar el documento al comprador."
    )
    d.parrafo(
        "Esa condición de proveedor es la que explica por qué la calidad, en este "
        "proyecto, no admite el tratamiento habitual. Un defecto en un sistema de gestión "
        "corriente afecta a quien lo usa, mientras que aquí un defecto se reproduce en "
        f"todas las empresas integradas y en todos los documentos que emiten. Además, la "
        f"factura electrónica es un documento con efectos legales y su contenido está "
        f"reglado por la autoridad tributaria ({cita('dian42')}), así que un error de "
        "cálculo, de numeración o de identificación del emisor no produce una molestia "
        "para el usuario sino un documento rechazado o, peor, aceptado diciendo algo que "
        "no corresponde. La calidad aquí es una condición para operar y no un atributo "
        "deseable del producto."
    )
    d.parrafo(
        "El informe se organiza en cuatro partes. La primera revisa los modelos y "
        "estándares de calidad vigentes, distinguiendo los que miran el producto de los "
        "que miran el proceso. La segunda declara cuáles se adoptaron para FactuGest, con "
        "el motivo por el que se descartaron los demás, y cruza el estándar elegido contra "
        "los requisitos no funcionales del sistema. La tercera presenta el plan de pruebas, "
        "con su alcance, su entorno, sus criterios y sus riesgos. La cuarta detalla las "
        "pruebas ejecutadas, con sus casos y resultados, las que quedan planificadas y los "
        "defectos que el proceso permitió encontrar y corregir."
    )


def _definiciones(d):
    d.titulo("2. Marco de calidad del software", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Antes de elegir un referente conviene fijar cuatro términos que el lenguaje "
        "corriente usa como equivalentes y que en este campo no lo son, pues de la "
        "diferencia entre modelo y estándar depende buena parte de lo que se decide en el "
        "capítulo siguiente."
    )

    d.titulo("2.1 Calidad y calidad de software", nivel=2)
    d.parrafo(
        f"La palabra calidad es ambigua y depende de quién observa, razón por la cual el "
        f"primer trabajo de cualquier marco es volverla medible. {narrativa('vega')} lo plantean "
        "en una frase que sirve de punto de partida, «pues si la calidad no puede ser "
        "definida, no puede ser medida; y donde la calidad no puede ser medida, entonces "
        "no puede ser controlada» (p. 145). El diccionario recoge el uso común del término "
        f"como el conjunto de propiedades inherentes que permiten juzgar el valor de algo "
        f"({cita('rae')}), lo que confirma el problema más que resolverlo, ya que juzgar el "
        "valor de un programa exige decir antes contra qué se lo juzga."
    )
    d.parrafo(
        f"Aplicada al software, la definición más citada es la de {narrativa('pressman')}, para "
        "quien la calidad es «la concordancia con los requerimientos funcionales y de "
        "rendimiento explícitamente establecidos, con los estándares de desarrollo "
        "explícitamente documentados y con las características implícitas que se espera de "
        "todo software desarrollado profesionalmente» (p. 294). La definición tiene tres "
        "partes y las tres cuentan, porque un producto puede cumplir lo que se le pidió, "
        "hacerlo sin seguir ninguna práctica reconocida y fallar en lo que nadie escribió "
        "porque se daba por supuesto."
    )
    d.parrafo(
        f"La norma ISO/IEC 9126 la define como la totalidad de características de un "
        f"producto de software que le dan la capacidad de satisfacer necesidades explícitas "
        f"o implícitas del cliente ({cita('iso9126')}), y el IEEE, como el grado con el que "
        f"un sistema, componente o proceso cumple los requisitos especificados y las "
        f"expectativas del usuario ({cita('ieee')}). Las tres definiciones coinciden en algo "
        "que conviene retener, y es que la calidad no se mide contra un ideal abstracto "
        "sino contra requisitos declarados, de modo que un proyecto sin requisitos escritos "
        "no tiene forma de afirmar que su producto tiene calidad. Conviene además la "
        f"advertencia que recoge {narrativa('gomez')} al citar a Mike Bria, según la cual la "
        "calidad se refiere a la ausencia de defectos antes que a la presencia de valor, "
        "pues son dos cosas que suelen confundirse al evaluar un producto."
    )

    d.titulo("2.2 Modelo y estándar", nivel=2)
    d.parrafo(
        f"Un modelo es un esquema teórico que explica una realidad compleja para facilitar "
        f"su comprensión y su estudio ({cita('rae')}). En calidad de software, un modelo "
        f"integra buenas prácticas, señala los temas en los que una organización debe poner "
        f"énfasis y permite medir los avances ({cita('scalone')}). Un estándar, en cambio, "
        "es un conjunto de guías o patrones adoptados por consenso y validados por una o "
        "varias entidades acreditadas, cuya función es que todos los procesos se realicen "
        "de la misma forma."
    )
    d.parrafo(
        "La diferencia práctica es de origen y de exigibilidad. El modelo propone y "
        "ordena, mientras que el estándar norma y permite comparar, certificar y exigir "
        "contractualmente. Para el proyecto esto tiene una consecuencia inmediata, porque "
        "un modelo se puede adoptar parcialmente y adaptar sin faltar a nada, mientras que "
        "un estándar se cumple o no se cumple, y afirmar que se cumple obliga a poder "
        "mostrar cómo."
    )


def _clasificacion(d):
    d.titulo("2.3 Clasificación por producto y por proceso", nivel=2)
    d.parrafo(
        "Modelos y estándares se dividen además según lo que observan. Los de producto "
        "miran el software terminado y sus atributos, mientras que los de proceso miran la "
        "forma de trabajar de la organización que lo construye, bajo el supuesto de que un "
        "proceso maduro produce productos consistentes. Las dos miradas son complementarias "
        "y ninguna sustituye a la otra, ya que un proceso impecable no garantiza que el "
        "producto sirva y un producto correcto puede haber salido de un proceso irrepetible."
    )
    d.tabla(
        "Clasificación de los modelos y estándares de calidad del software",
        ["Ámbito", "Modelos", "Estándares"],
        [["Producto",
          "McCall (1977), Boehm (1978), FURPS, Dromey",
          "ISO/IEC 9126, ISO/IEC 25000 SQuaRE, ISO/IEC 25010"],
         ["Proceso",
          "CMM, CMMI, Bootstrap, PSP, TSP, Six Sigma para software",
          "ISO/IEC 15504 SPICE, ISO 9001, ISO/IEC 12207, TickIT"]],
        nota=f"Adaptado de {cita('scalone')} y del material de formación "
             f"({cita('sena')}). Se destacan en el texto los que se estudian en este "
             "informe.",
        anchos=[2.4, 6.0, 6.4],
    )
    d.parrafo(
        "El informe estudia los cinco que el material de formación desarrolla, que son los "
        "modelos de McCall y Boehm y el modelo de proceso CMMI, junto con los estándares "
        "ISO/IEC 9126, ISO/IEC 25000, ISO/IEC 25010, ISO/IEC 15504 e ISO 9001. Sobre esa "
        "revisión se decide en el capítulo 3."
    )


def _modelos_producto(d):
    d.titulo("2.4 Modelos de calidad a nivel de producto", nivel=2)

    d.titulo("2.4.1 Modelo de McCall", nivel=3)
    d.parrafo(
        f"Desarrollado en 1977 por Jim McCall para la fuerza aérea de los Estados Unidos, "
        f"busca reducir la distancia entre usuarios y desarrolladores tomando en cuenta "
        f"factores de calidad en los que estén presentes las necesidades de ambos "
        f"({cita('estayno')}). Su propuesta es especificar los requisitos de calidad al "
        "comenzar el proyecto y en cada etapa del ciclo de vida, fijando para cada factor "
        "un valor deseable que al final se comprueba, lo que lo convierte en el primer "
        "modelo que trata la calidad como algo que se planea y no como algo que se revisa "
        "al terminar."
    )
    d.parrafo(
        "El modelo organiza once factores en tres ejes o puntos de vista desde los cuales "
        "el usuario puede observar el producto, y cada factor se descompone en criterios "
        "que se evalúan mediante métricas con valores máximos y mínimos."
    )
    d.tabla(
        "Los once factores de calidad del modelo de McCall",
        ["Eje", "Qué observa", "Factores"],
        [["Operación del producto", "Cómo se comporta mientras se usa",
          "Corrección, fiabilidad, eficiencia, integridad y facilidad de uso"],
         ["Revisión del producto", "Qué tan fácil es corregirlo y adaptarlo",
          "Facilidad de mantenimiento, flexibilidad y facilidad de prueba"],
         ["Transición del producto", "Qué tan bien se mueve a otro entorno",
          "Portabilidad, reusabilidad e interoperabilidad"]],
        nota=f"Adaptado de {cita('pressman')} y {cita('estayno')}.",
        anchos=[4.2, 5.0, 5.6],
    )
    d.parrafo(
        "Su límite es conocido y conviene anotarlo, porque varios de sus factores no "
        "tienen métrica directa y terminan evaluándose con listas de comprobación "
        "subjetivas. Aun así, la partición en tres ejes sigue siendo útil como forma de "
        "ordenar la conversación sobre qué se le va a exigir a un producto."
    )

    d.titulo("2.4.2 Modelo de Boehm", nivel=3)
    d.parrafo(
        "Presentado por Barry Boehm en 1978, es el segundo más reconocido y se organiza en "
        "tres niveles que van de lo general a lo medible. En el nivel alto están los "
        "requerimientos generales de uso, en el intermedio los factores de calidad "
        "propiamente dichos y en el primitivo las características asociadas de forma "
        "directa a una o dos métricas."
    )
    d.tabla(
        "Los tres niveles del modelo de Boehm",
        ["Nivel", "Contenido"],
        [["Alto",
          "Utilidad per se, o qué tan usable, confiable y eficiente es el producto en sí "
          "mismo. Mantenibilidad, o qué tan fácil es entenderlo, modificarlo y volverlo a "
          "probar. Utilidad general, o si puede seguir usándose al cambiar el entorno"],
         ["Intermedio",
          "Portabilidad, confiabilidad, eficiencia, usabilidad, testeabilidad, facilidad "
          "de entendimiento y modificabilidad"],
         ["Primitivo",
          "Características medibles de forma directa, que son las que alimentan las "
          "métricas del nivel superior"]],
        nota=f"Adaptado del material de formación ({cita('sena')}).",
        anchos=[2.8, 12.0],
    )
    d.parrafo(
        "Frente a McCall, el aporte de Boehm es la trazabilidad entre niveles, ya que cada "
        "característica general se sostiene en otras que sí se pueden medir. Es la idea que "
        "recogen después los estándares ISO, donde cada característica se descompone en "
        "subcaracterísticas y estas en métricas."
    )


def _modelo_proceso(d):
    d.titulo("2.5 Modelo de calidad a nivel de proceso", nivel=2)
    d.parrafo(
        "A nivel de proceso existen varios referentes, entre ellos CMM y su sucesor CMMI, "
        "Bootstrap, TickIT, el proceso personal de software, el proceso de software en "
        "equipo y Six Sigma para software. El material de formación desarrolla CMMI por su "
        "incidencia en el mercado, y es el que se revisa aquí."
    )

    d.titulo("2.5.1 CMMI", nivel=3)
    d.parrafo(
        f"El modelo de integración de madurez de capacidades es un enfoque de mejora de "
        f"procesos publicado en el año 2000 por el Instituto de Ingeniería de Software de "
        f"la Universidad Carnegie Mellon ({cita('cmmi')}). Permite a una organización "
        "determinar la madurez de sus procesos actuales, identificar los elementos críticos "
        "para el aseguramiento de la calidad y reconocer las prácticas clave que necesita "
        "incorporar para mejorar. A diferencia de CMM, que estaba pensado sobre el modelo "
        "en cascada, CMMI se formuló para los modelos de desarrollo iterativos que se usan "
        "hoy, y esa es la razón por la que sigue siendo aplicable a un proyecto que trabaja "
        "por iteraciones."
    )
    d.tabla(
        "Los cinco niveles de madurez de CMMI",
        ["Nivel", "Nombre", "Qué caracteriza a la organización"],
        [["1", "Inicial",
          "Los procesos son caóticos y el resultado depende del esfuerzo de las personas"],
         ["2", "Gestionado",
          "Hay conciencia de la dirección y los procesos se planifican y se controlan por "
          "proyecto"],
         ["3", "Definido",
          "Los procesos están caracterizados, comprendidos y son los mismos en toda la "
          "organización"],
         ["4", "Gestión cuantitativa",
          "Se establecen objetivos medibles de rendimiento y calidad del proceso"],
         ["5", "En optimización",
          "La mejora es continua y se apoya en la comprensión cuantitativa de los "
          "resultados"]],
        nota=f"Adaptado de {cita('cmmi')} y del material de formación ({cita('sena')}).",
        anchos=[1.6, 4.0, 9.2],
    )
    d.parrafo(
        "Para un equipo de formación el valor de CMMI no está en la certificación, que "
        "supone una evaluación formal fuera del alcance de este proyecto, sino en el orden "
        "que propone. El nivel 2 describe prácticas que un equipo pequeño sí puede "
        "sostener, como la gestión de requisitos, la planificación y el seguimiento del "
        "trabajo, la gestión de configuración y el aseguramiento de la calidad del producto "
        "y del proceso, y es contra ese nivel que el capítulo 3 contrasta lo que el "
        "proyecto ya hace."
    )


def _estandares_producto(d):
    d.titulo("2.6 Estándares de calidad a nivel de producto", nivel=2)

    d.titulo("2.6.1 ISO/IEC 9126", nivel=3)
    d.parrafo(
        f"Publicado en 2001 y revisado en 2004, evalúa la calidad del producto a partir de "
        f"seis características que se descomponen en subcaracterísticas y que se observan "
        f"tanto de forma interna, sobre los atributos propios del producto, como externa, "
        f"sobre su comportamiento al ejecutarse ({cita('iso9126')}). Es el primer estándar "
        "que da una terminología común para hablar de calidad de producto, y por eso sus "
        "seis características siguen reconociéndose en los modelos posteriores."
    )
    d.tabla(
        "Las seis características de calidad de la norma ISO/IEC 9126",
        ["Característica", "Subcaracterísticas"],
        [["Funcionalidad",
          "Adecuación, exactitud, interoperabilidad, seguridad de acceso y cumplimiento"],
         ["Fiabilidad",
          "Madurez, tolerancia a fallos, capacidad de recuperación y cumplimiento"],
         ["Usabilidad",
          "Capacidad de ser entendido, aprendido y operado, atractivo y cumplimiento"],
         ["Eficiencia",
          "Comportamiento temporal, utilización de recursos y cumplimiento"],
         ["Mantenibilidad",
          "Capacidad de ser analizado, cambiado y probado, estabilidad y cumplimiento"],
         ["Portabilidad",
          "Adaptabilidad, instalabilidad, coexistencia, reemplazabilidad y cumplimiento"]],
        nota=f"Adaptado de {cita('fillottrani')} y {cita('iso9126')}.",
        anchos=[4.0, 10.8],
    )

    d.titulo("2.6.2 ISO/IEC 25000 SQuaRE", nivel=3)
    d.parrafo(
        f"La familia ISO/IEC 25000, conocida como SQuaRE por sus siglas en inglés, "
        f"reemplaza y unifica las normas ISO/IEC 9126 e ISO/IEC 14598, y su objetivo es "
        f"guiar el desarrollo de productos de software mediante la especificación y la "
        f"evaluación de requisitos de calidad ({cita('iso25000')}; {cita('portal25000')}). "
        "Su aporte es organizar en un solo marco lo que antes estaba repartido, pues define "
        "el modelo de calidad, la forma de medirlo, la manera de escribir los requisitos y "
        "el proceso para evaluarlos."
    )
    d.tabla(
        "Las cinco divisiones de la familia ISO/IEC 25000",
        ["División", "Nombre", "Qué contiene"],
        [["ISO 2500n", "Gestión de la calidad",
          "Términos, definiciones y modelos de referencia comunes a toda la familia"],
         ["ISO 2501n", "Modelo de calidad",
          "Las características y subcaracterísticas del producto y de la calidad en uso"],
         ["ISO 2502n", "Medida de la calidad",
          "Las métricas con las que se cuantifica cada característica"],
         ["ISO 2503n", "Requisitos de calidad",
          "Cómo se especifican los requisitos que después se van a evaluar"],
         ["ISO 2504n", "Evaluación de la calidad",
          "El proceso de evaluación y los requisitos para quien evalúa"]],
        nota=f"Adaptado de {cita('alfonzo')} y {cita('portal25000')}.",
        anchos=[2.8, 4.2, 7.8],
    )

    d.titulo("2.6.3 ISO/IEC 25010", nivel=3)
    d.parrafo(
        f"Publicada en 2011 dentro de la división 2501n, reemplaza y actualiza el modelo de "
        f"la norma ISO/IEC 9126 ({cita('iso25010')}). Define dos modelos complementarios. El "
        f"modelo de calidad del producto se compone de ocho características y treinta y una "
        f"subcaracterísticas, y se refiere a las propiedades estáticas del software y "
        f"dinámicas del sistema. El modelo de calidad en uso se compone de cinco "
        f"características y nueve subcaracterísticas, y describe el resultado de la "
        f"interacción cuando el producto se emplea en un contexto particular "
        f"({cita('polillo')})."
    )
    d.tabla(
        "Las ocho características del modelo de calidad de producto de la norma ISO/IEC 25010",
        ["Característica", "Subcaracterísticas"],
        [["Adecuación funcional",
          "Completitud, corrección y pertinencia funcional"],
         ["Eficiencia de desempeño",
          "Comportamiento temporal, utilización de recursos y capacidad"],
         ["Compatibilidad",
          "Coexistencia e interoperabilidad"],
         ["Usabilidad",
          "Capacidad de reconocer su adecuación, de aprendizaje y de ser usado, protección "
          "contra errores de usuario, estética de la interfaz y accesibilidad"],
         ["Fiabilidad",
          "Madurez, disponibilidad, tolerancia a fallos y capacidad de recuperación"],
         ["Seguridad",
          "Confidencialidad, integridad, no repudio, responsabilidad y autenticidad"],
         ["Mantenibilidad",
          "Modularidad, reusabilidad, analizabilidad, capacidad de ser modificado y de ser "
          "probado"],
         ["Portabilidad",
          "Adaptabilidad, facilidad de instalación y capacidad de ser reemplazado"]],
        nota=f"Adaptado de {cita('iso25010')}. Las cinco características del modelo de "
             "calidad en uso son efectividad, eficiencia, satisfacción, ausencia de riesgo "
             "y cobertura del contexto.",
        anchos=[4.0, 10.8],
    )
    d.parrafo(
        "Frente a la norma ISO/IEC 9126, los cambios que más pesan para un sistema como "
        "este son dos. La seguridad deja de ser una subcaracterística escondida dentro de "
        "la funcionalidad y pasa a ser una característica propia con cinco "
        "subcaracterísticas, y aparece la compatibilidad, que es donde cae la capacidad de "
        "un sistema de operar junto a otros y de intercambiar información con ellos. Para "
        "una plataforma cuyo producto principal es una interfaz de integración consumida "
        "por sistemas ajenos, esas dos características no son un detalle de la "
        "actualización sino la razón para preferirla."
    )


def _estandares_proceso(d):
    d.titulo("2.7 Estándares de calidad a nivel de proceso", nivel=2)

    d.titulo("2.7.1 ISO/IEC 15504 SPICE", nivel=3)
    d.parrafo(
        f"Es un marco de evaluación y mejora de los procesos de desarrollo y mantenimiento "
        f"de software, más utilizado en Europa, que cubre tres áreas, la mejora de "
        f"procesos, la evaluación de procesos y la determinación de la capacidad "
        f"({cita('iso15504')}). Está alineado con la norma ISO/IEC 12207, que define los "
        f"procesos del ciclo de vida del software ({cita('iso12207')}), y provee nueve "
        "documentos que guían la implementación del modelo y su evaluación. Su "
        "particularidad frente a CMMI es que se concentra en establecer un marco para "
        "evaluar antes que en prescribir un método de trabajo."
    )

    d.titulo("2.7.2 ISO 9001", nivel=3)
    d.parrafo(
        f"Pertenece a la familia ISO 9000 de sistemas de gestión de la calidad y se aplica "
        f"a cualquier organización, no solo a las que desarrollan software "
        f"({cita('iso9001')}). Su versión de 2015 se apoya en el enfoque a procesos, el "
        "pensamiento basado en riesgos y la orientación a las necesidades del cliente. Es "
        "un referente de gestión organizacional, de modo que aporta a la forma de trabajar "
        "de una empresa de desarrollo, pero no dice nada sobre los atributos que debe tener "
        "un programa, y esa distinción es la que se retoma en el capítulo siguiente."
    )
