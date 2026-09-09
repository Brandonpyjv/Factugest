"""
AA1, capítulos 6, 7 y 8. Pruebas planificadas, resultados y conclusiones.

El capítulo 6 es el que la guía habilita al pedir las pruebas «ejecutadas o
planificadas». Se escribe con la misma exigencia que el anterior, o sea con su
métrica objetivo y su condición de inicio, porque una prueba planificada sin
criterio de aprobación no es un plan sino una intención.

El capítulo 7 es el que un evaluador lee con más atención, y por eso no se limita a
decir que todo pasó. Lo que aporta son los cuatro defectos que el proceso encontró,
y sobre todo el patrón que forman, pues los cuatro aparecieron en la parte del
sistema que no tenía pruebas y ninguno en la que sí las tenía.
"""
from evidencia import (DEFECTOS, FUNCIONALES, INTEGRACION, INVARIANTES, PENDIENTES,
                       TOTAL_UNITARIAS, UNITARIAS)
from fuentes import cita, narrativa

CITADAS = ["istqb", "iso29119", "iso25010", "dian42", "myers", "beck"]

# (prueba, qué se mediría, métrica de aprobación, qué hace falta para ejecutarla)
PLANIFICADAS = [
    ("Carga sobre la emisión",
     "El tiempo de respuesta de la emisión con varias peticiones simultáneas",
     "El 95 % de las emisiones por debajo de tres segundos, sin ninguna respuesta "
     "errónea ni ningún consecutivo repetido",
     "Un servidor de pruebas separado del equipo de desarrollo y una herramienta de "
     "carga"),
    ("Concurrencia sobre la numeración",
     "Que dos peticiones simultáneas del mismo emisor no obtengan el mismo número",
     "Ningún número repetido en varias emisiones lanzadas a la vez",
     "El mismo servidor de pruebas. Hoy el riesgo está cubierto por diseño, con la "
     "reserva en una sola sentencia y el índice único"),
    ("Análisis de dependencias",
     "Las bibliotecas de terceros que usa el sistema y sus vulnerabilidades conocidas",
     "Ninguna vulnerabilidad de severidad alta sin tratar",
     "Una herramienta de análisis y la decisión de con qué periodicidad se corre"),
    ("Pruebas dirigidas de entrada",
     "El comportamiento de la interfaz ante datos malformados, desbordados o "
     "maliciosos",
     "Ninguna entrada que provoque un error del programa en lugar de un rechazo "
     "controlado",
     "Ampliar la colección de peticiones con los casos de abuso"),
    ("Regresión automática",
     "Que la batería completa se ejecute sola con cada cambio integrado",
     "Ningún cambio integrado con la batería en rojo",
     "Un servicio de integración continua sobre el repositorio"),
    ("Validación con el proveedor habilitado",
     "Que un documento real sea aceptado por la autoridad tributaria",
     "Acuse de recibo y aceptación del documento transmitido",
     "El acuerdo formalizado con un proveedor tecnológico habilitado"),
    ("Usabilidad después del uso",
     "La satisfacción de quien usa el sistema a diario, medida con instrumento",
     "Una calificación media que permita comparar entre versiones",
     "Usuarios reales operando el sistema durante un periodo"),
]

# (defecto, severidad, cómo se detectó, qué lo cubre hoy)
DETALLE_DEFECTOS = [
    ("El documento salía con el membrete del proveedor y no con el de la empresa que "
     "emitía", "Crítica",
     "Revisión de un documento generado por la interfaz de integración",
     "Diez pruebas automatizadas, una de las cuales comprueba que el nombre del "
     "proveedor no aparezca en ninguna parte del documento de un tercero"),
    ("El pie mostraba un descuento del 0,0 % restando dinero real", "Mayor",
     "Lectura de una factura con descuento por producto",
     "Seis pruebas automatizadas sobre las filas de descuento del pie"),
    ("La ciudad y el departamento del comprador salían vacíos en todo lo emitido por la "
     "interfaz", "Mayor",
     "Lectura del documento generado, donde la dirección se leía como si fuera la ciudad",
     "Verificación sobre el documento emitido, pues comprobarlo de forma automatizada "
     "exige base de datos"),
    ("Las columnas de dinero partían los importes de ocho cifras", "Menor",
     "Revisión de una factura de importe alto",
     "El ancho se calcula midiendo el peor caso, y el espacio se toma de la columna que "
     "puede repartirse en varias líneas"),
]

# (acción de mejora, qué corrige, cuándo)
MEJORA = [
    ("Automatizar la ejecución de la batería con cada cambio integrado",
     "Que una corrección rompa algo probado y nadie se entere hasta la siguiente corrida",
     "Junto con el despliegue"),
    ("Extender las pruebas automatizadas a la capa que consulta la base de datos",
     "Que los defectos aparezcan justamente donde no hay pruebas, que es lo que ocurrió "
     "con los cuatro encontrados",
     "Antes del despliegue"),
    ("Medir el tiempo de respuesta de la emisión bajo carga",
     "Que el primer requisito no funcional siga siendo una intención y no una medida",
     "Junto con el despliegue"),
    ("Incorporar el análisis de dependencias a la rutina",
     "Que una biblioteca con una vulnerabilidad conocida entre sin que nadie lo note",
     "Antes del despliegue"),
    ("Formalizar el acuerdo con un proveedor tecnológico habilitado",
     "Que la transmisión real ante la autoridad tributaria siga fuera del alcance",
     "Fase siguiente del proyecto"),
    ("Aplicar el instrumento de usabilidad después de un periodo de uso",
     "Que la usabilidad se sostenga en decisiones de diseño y no en una medida",
     "Con el sistema en operación"),
]


def escribir(d):
    _planificadas(d)
    _resultados(d)
    _defectos(d)
    _cobertura(d)
    _conclusiones(d)


def _planificadas(d):
    d.titulo("6. Pruebas planificadas", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Lo que sigue no se ha ejecutado y se declara con esas palabras. La guía admite "
        "presentar pruebas ejecutadas o planificadas, y presentar como ejecutado lo que no "
        "se hizo invalidaría también lo que sí, porque un informe de pruebas vale "
        "exactamente lo que valga su parte menos verificable."
    )
    d.parrafo(
        "Cada prueba planificada se escribe con su métrica de aprobación y con lo que hace "
        f"falta para poder ejecutarla ({cita('iso29119')}). Sin métrica no hay forma de "
        "saber si una prueba de rendimiento salió bien, y sin la condición de inicio la "
        "planificación se convierte en una lista de buenas intenciones que nadie puede "
        "programar."
    )
    d.tabla(
        "Pruebas planificadas, su métrica de aprobación y su condición de inicio",
        ["Prueba", "Qué se mediría", "Métrica de aprobación", "Qué hace falta"],
        [[prueba, mide, metrica, requisito]
         for prueba, mide, metrica, requisito in PLANIFICADAS],
        nota="Ninguna de las siete se ha ejecutado a la fecha de este informe. Las cuatro "
             "primeras dependen de un entorno de pruebas separado y las tres últimas, de "
             "decisiones que exceden al equipo de desarrollo.",
        anchos=[3.0, 4.0, 4.2, 3.6],
    )
    d.parrafo(
        "La segunda merece una precisión, porque podría parecer que un riesgo conocido "
        "quedó sin atender. La prueba de concurrencia sobre la numeración está planificada, "
        "pero el riesgo que mediría ya está cubierto por el diseño, con la reserva del "
        "consecutivo resuelta en una sola sentencia y un índice único que la base de datos "
        "hace cumplir. La prueba serviría para confirmar el comportamiento bajo carga real, "
        "no para descubrir si el problema existe."
    )
    d.parrafo(
        f"La última de la tabla es la que más depende de algo ajeno al equipo. La "
        f"transmisión real exige un proveedor tecnológico habilitado por la autoridad "
        f"tributaria ({cita('dian42')}), y mientras ese acuerdo no exista, lo que se puede "
        "verificar es que el sistema produce lo que ese proveedor va a recibir. Eso sí está "
        "hecho, con las veinticuatro pruebas del adaptador que fijan el contrato esperado, "
        "de modo que una diferencia con el proveedor real aparecerá el primer día de la "
        "integración y no en producción."
    )


def _resultados(d):
    d.titulo("7. Resultados", nivel=1, nueva_pagina=True)
    d.parrafo(
        f"La ejecución cerró sin fallas. Las {TOTAL_UNITARIAS} pruebas automatizadas de "
        f"los {len(UNITARIAS)} archivos terminaron en verde, las {len(INTEGRACION)} "
        f"peticiones de la interfaz respondieron con el código y la forma documentados, y "
        f"las {len(FUNCIONALES)} operaciones funcionales se completaron con su registro en "
        "imagen. No queda ningún defecto de severidad crítica ni mayor abierto."
    )
    d.parrafo(
        "Ese resultado, por sí solo, dice menos de lo que parece. Una batería que siempre "
        "está en verde puede significar que el sistema funciona o que las pruebas no "
        f"buscan donde duele ({narrativa('myers')}), de modo que lo que sigue no es el "
        "recuento de lo que pasó sino el de lo que falló mientras se construía, que es "
        "donde se ve si el proceso de calidad sirvió para algo."
    )


def _defectos(d):
    d.titulo("7.1 Defectos encontrados y corregidos", nivel=2)
    d.parrafo(
        f"Durante la construcción se encontraron y corrigieron {len(DEFECTOS)} defectos "
        "que vale la pena documentar, no porque sean todos los que hubo, sino porque los "
        "cuatro afectaban al documento que el cliente recibe y tres de ellos habrían "
        "llegado al usuario final sin que ninguna prueba los detuviera."
    )
    d.tabla(
        "Defectos encontrados durante la construcción y su tratamiento",
        ["Defecto", "Severidad", "Cómo se detectó", "Qué lo cubre hoy"],
        [[defecto, severidad, deteccion, cobertura]
         for defecto, severidad, deteccion, cobertura in DETALLE_DEFECTOS],
        nota="Los cuatro están corregidos. La severidad corresponde a la clasificación "
             "declarada en el plan de pruebas.",
        anchos=[4.2, 1.8, 3.6, 5.2],
    )
    d.parrafo(
        "El primero es el más grave que este sistema puede producir y conviene explicar "
        "por qué. Los documentos emitidos por la interfaz de integración traen su emisor "
        "aparte, y ese dato no llegaba al generador de la representación gráfica, que caía "
        "entonces en sus valores por defecto. El resultado era que la factura de una "
        "clínica salía con el nombre y el logotipo del proveedor tecnológico, como si la "
        "hubiera expedido este. Una factura que dice quién la expidió, nombrando a la "
        "empresa equivocada, es un documento que no sirve para lo que existe."
    )

    d.titulo("7.2 Lo que los defectos tienen en común", nivel=2)
    d.parrafo(
        "El patrón que forman los cuatro es más útil que cada uno por separado. Ninguno "
        "está en la aritmética tributaria, que es la parte del sistema que se escribió con "
        "pruebas desde el principio, y los cuatro están en la generación del documento y "
        "en la consulta que lo alimenta, que es la parte que no las tenía. Dicho de otro "
        "modo, los defectos aparecieron exactamente donde no se estaba mirando."
    )
    d.parrafo(
        "De ahí salen dos consecuencias que este informe recoge. La primera es la regla "
        "que el plan ya declara, según la cual un defecto se reproduce primero con una "
        "prueba que falla y solo después se corrige, de modo que hoy dieciséis pruebas "
        "cubren dos de esos cuatro defectos y ninguno puede volver en silencio "
        f"({narrativa('beck')}). La segunda es la primera acción del plan de mejora, que "
        "consiste en extender la automatización a la capa que consulta la base de datos, "
        "porque el tercer defecto, la ciudad del comprador que llegaba vacía, sigue sin "
        "prueba automatizada justamente por vivir en esa capa."
    )


def _cobertura(d):
    d.titulo("7.3 Cobertura frente al modelo de calidad adoptado", nivel=2)
    d.parrafo(
        "Cruzando lo ejecutado con las ocho características del capítulo 3, seis quedan "
        f"respaldadas con evidencia de ejecución y dos lo están solo en parte "
        f"({cita('iso25010')}). La eficiencia de desempeño tiene resueltas por diseño sus "
        "tres exigencias, con el correo fuera de la respuesta y los listados paginados, "
        "pero le falta la medición del tiempo bajo carga. La fiabilidad tiene probada la "
        "atomicidad de la emisión y la independencia frente a la caída del correo, pero su "
        "requisito de disponibilidad solo puede verificarse con el sistema desplegado."
    )
    d.parrafo(
        "Conviene añadir que parte de lo que sostiene la calidad de este sistema no son "
        "pruebas sino invariantes, o sea reglas que el diseño impide romper. Están escritas "
        "en la documentación técnica del proyecto y son las que explican por qué ciertos "
        "errores no pueden ocurrir en lugar de por qué no ocurrieron."
    )
    d.tabla(
        "Invariantes del sistema que el diseño hace cumplir",
        ["Invariante", "Qué garantiza"],
        [[nombre, descripcion] for nombre, descripcion in INVARIANTES],
        nota="Un invariante es más fuerte que una prueba, porque la prueba comprueba un "
             "caso y el invariante impide todos. La reserva del consecutivo es el ejemplo "
             "claro, ya que el índice único de la base rechaza el segundo documento "
             "aunque el programa se equivoque.",
        anchos=[3.4, 11.4],
    )


def _conclusiones(d):
    d.titulo("8. Conclusiones y plan de mejora", nivel=1, nueva_pagina=True)
    d.parrafo(
        "El trabajo de calidad sobre FactuGest permite sostener cinco conclusiones."
    )
    d.numerada([
        "La norma ISO/IEC 25010 resultó aplicable al proyecto sin forzarla, y el cruce "
        "con el catálogo propio dejó las ocho características cubiertas. El reparto "
        "resultante, con la seguridad concentrando la mayor parte de los requisitos, "
        "describe con precisión lo que significa operar como proveedor tecnológico, y no "
        "es un resultado que se hubiera podido anticipar sin hacer el cruce.",

        "Adoptar un referente externo obligó a renombrar tres categorías propias que "
        "parecían correctas. La trazabilidad resultó ser responsabilidad y no repudio, y "
        "la escalabilidad se repartió entre capacidad e interoperabilidad, lo que muestra "
        "que el vocabulario común de un estándar no es un formalismo sino una forma de "
        "clasificar mejor lo que ya se tenía.",

        "La automatización cumplió su función donde se aplicó. Las pruebas de la "
        "aritmética tributaria, escritas con valores calculados a mano, no dejaron pasar "
        "ningún defecto de cálculo, que es la clase de error más costosa en un documento "
        "con efectos tributarios.",

        "Los cuatro defectos documentados aparecieron en la parte del sistema que no "
        "tenía pruebas, lo que confirma que la cobertura no es un indicador decorativo. "
        "El más grave de todos, el membrete con el emisor equivocado, no habría producido "
        "un error visible en ninguna pantalla, y por eso solo aparece cuando alguien "
        "revisa el documento resultante.",

        "El aseguramiento de la calidad no se sostiene únicamente en pruebas. Los "
        "invariantes de numeración, atomicidad y cálculo único impiden clases enteras de "
        "error que una prueba solo podría detectar caso por caso, y son la respuesta "
        "correcta para lo que depende de la concurrencia.",
    ])
    d.parrafo(
        "De las pruebas planificadas y de lo aprendido en las ejecutadas sale el plan de "
        "mejora, ordenado por lo que más reduce el riesgo y no por lo que cuesta menos."
    )
    d.tabla(
        "Plan de mejora continua",
        ["Acción", "Qué riesgo corrige", "Cuándo"],
        [[accion, riesgo, cuando] for accion, riesgo, cuando in MEJORA],
        nota="Las dos primeras acciones salen de los defectos encontrados y no de una "
             "lista general de buenas prácticas.",
        anchos=[4.6, 6.4, 3.8],
    )
    d.parrafo(
        f"Queda por último una observación sobre el alcance de todo lo anterior "
        f"({cita('istqb')}). Ninguna de estas pruebas demuestra que FactuGest esté libre "
        "de defectos, porque eso no es algo que las pruebas puedan demostrar. Lo que "
        f"sostienen las {TOTAL_UNITARIAS} pruebas automatizadas, las peticiones sobre la "
        "interfaz, las operaciones verificadas en pantalla y los invariantes del diseño es "
        "algo más modesto y más útil, y es que los errores que ya se cometieron una vez no "
        "pueden volver sin que alguien se entere."
    )
