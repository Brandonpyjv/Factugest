"""
AA1, capítulo 4. El plan de pruebas.

Es la parte que la guía pide de forma explícita, «el plan de pruebas utilizado para
validar su correcto funcionamiento», y la que la instructora resumió como el informe
de pruebas del proyecto productivo.

El plan se escribe con la estructura habitual de la documentación de pruebas, con su
alcance, su entorno, sus criterios y sus riesgos, pero describe lo que este proyecto
hizo de verdad. Donde algo no se ejecutó, se dice que está planificado y no se
disfraza de ejecutado, que es la única forma de que el capítulo siguiente sirva de
evidencia.

Las cifras vienen de `evidencia.py`, así que este archivo no repite ningún número.
"""
from evidencia import (CARPETA_CAPTURAS, COLECCION, DURACION, FUNCIONALES, HERRAMIENTA,
                       INTEGRACION, RNF, TOTAL_UNITARIAS, UNITARIAS)
from fuentes import cita, narrativa

CITADAS = ["istqb", "ieee829", "iso29119", "myers", "beck", "iso25010", "dian42"]

# (nivel, qué verifica, técnica, con qué se ejecuta, estado)
NIVELES = [
    ("Unitaria",
     "Una función o un servicio aislado, sin base de datos ni servidor",
     "Caja blanca, con partición de equivalencia y valores límite",
     "pytest",
     "Ejecutada"),
    ("Integración",
     "El recorrido completo de la interfaz de integración, desde la llave hasta la nota "
     "crédito",
     "Caja negra sobre el contrato publicado",
     "Colección de peticiones y documentación interactiva",
     "Ejecutada"),
    ("Sistema y funcional",
     "Las operaciones del panel de principio a fin, con la base de datos real",
     "Caja negra, por caso de uso",
     "Navegador, con registro en imagen",
     "Ejecutada"),
    ("Aceptación",
     "Que lo entregado corresponda a lo que el requisito pedía",
     "Revisión contra el catálogo de requisitos y los casos de uso",
     "Revisión del equipo",
     "Ejecutada"),
    ("Usabilidad",
     "Que la navegación y los mensajes sirvan a quien no construyó el sistema",
     "Encuesta a empresas y observación directa",
     "Instrumento de encuesta",
     "Ejecutada"),
    ("Seguridad",
     "El almacenamiento de credenciales, el control de acceso por rol y el cierre de "
     "sesión",
     "Inspección y prueba dirigida",
     "Revisión de la base y pruebas automatizadas",
     "Ejecutada en parte"),
    ("Rendimiento",
     "El tiempo de respuesta de la emisión bajo carga concurrente",
     "Prueba de carga",
     "Herramienta de carga, por definir",
     "Planificada"),
    ("Regresión",
     "Que una corrección no rompa lo que ya funcionaba",
     "Nueva ejecución de la batería completa",
     "pytest, hoy manual",
     "Ejecutada de forma manual"),
]

# (componente, qué se usa)
ENTORNO = [
    ("Sistema operativo", "Windows 11"),
    ("Lenguaje", "Python 3.13.3"),
    ("Marco de trabajo web", "FastAPI, servido con Uvicorn"),
    ("Base de datos", "MySQL, con el esquema aplicado por el migrador del proyecto"),
    ("Ejecutor de pruebas", "pytest 9.1.1"),
    ("Pruebas de la interfaz de integración",
     "Colección de peticiones y la documentación interactiva que publica el propio "
     "servidor"),
    ("Pruebas del panel", "Navegador de escritorio"),
    ("Datos", "Sembrador determinista del proyecto"),
]

# (severidad, qué la define, ejemplo real del proyecto)
SEVERIDADES = [
    ("Crítica",
     "Produce un documento inválido ante la autoridad tributaria, expone datos o impide "
     "facturar",
     "El PDF de un documento emitido por la interfaz de integración salía con el nombre y "
     "el logo del proveedor y no con los de la empresa que expedía"),
    ("Mayor",
     "El documento sale, pero dice algo que no se puede explicar o falta un dato "
     "obligatorio",
     "El pie de la factura mostraba un descuento del 0,0 % restando dinero real, y la "
     "ciudad del comprador salía vacía en todo lo emitido por la interfaz"),
    ("Menor",
     "El contenido es correcto pero su presentación estorba la lectura",
     "Las columnas de dinero partían los importes de ocho cifras, de modo que el impuesto "
     "quedaba con un dígito solitario en el renglón siguiente"),
]

# (riesgo, qué pasa si ocurre, cómo se atiende)
RIESGOS = [
    ("El entorno de pruebas no es el de producción",
     "Un defecto que solo aparece con concurrencia real o con volumen alto no se "
     "detecta antes de desplegar",
     "Los invariantes que dependen de la concurrencia, como la reserva del consecutivo, "
     "se resolvieron por diseño y no por prueba, con una sola sentencia y un índice único "
     "que la base hace cumplir"),
    ("No hay transmisión real ante la autoridad tributaria",
     "El comportamiento del proveedor habilitado podría diferir de lo que supone el "
     "adaptador",
     "El adaptador tiene 24 pruebas que fijan el contrato esperado, de modo que la "
     "diferencia se detecta el primer día de la integración real y no en producción"),
    ("El equipo es pequeño y no hay un probador independiente",
     "Quien escribió el código tiende a probar lo que pensó y no lo que puede fallar",
     "Las pruebas se escriben con valores calculados a mano y no copiados de la salida "
     "del programa, y cada integrante revisa lo que escribió otro"),
    ("Los datos de prueba son sembrados",
     "Un caso que la realidad produce y el sembrador no, queda sin probar",
     "El sembrador reproduce la operación de catorce empresas durante varios meses, y las "
     "pruebas unitarias no dependen de él porque no tocan la base de datos"),
    ("No hay ejecución automática en cada cambio",
     "Una corrección puede romper algo ya probado y nadie enterarse hasta la siguiente "
     "corrida",
     "La batería completa tarda segundos y se ejecuta antes de cerrar cada tarea. La "
     "ejecución automática queda planificada"),
]

# (rol, responsabilidad)
ROLES = [
    ("Analista de pruebas",
     "Deriva los casos del catálogo de requisitos y decide qué se prueba primero según el "
     "riesgo"),
    ("Desarrollador",
     "Escribe la prueba unitaria junto con el código que la satisface y la deja en la "
     "batería"),
    ("Probador",
     "Ejecuta las pruebas funcionales sobre lo que escribió otro integrante y levanta el "
     "registro en imagen"),
    ("Responsable de la corrección",
     "Reproduce el defecto con una prueba que falla, lo corrige y deja esa prueba como "
     "regresión"),
]


def escribir(d):
    _objetivo(d)
    _estrategia(d)
    _entorno(d)
    _criterios(d)
    _defectos(d)
    _riesgos(d)
    _roles(d)


def _objetivo(d):
    d.titulo("4. Plan de pruebas", nivel=1, nueva_pagina=True)
    d.parrafo(
        "El plan que sigue documenta cómo se verificó FactuGest. Se organiza con la "
        "estructura habitual de la documentación de pruebas, con su objetivo, su alcance, "
        f"su entorno, sus criterios y sus riesgos ({cita('ieee829')}; {cita('iso29119')}), "
        "y describe lo que el proyecto hizo, de modo que cada nivel declarado como "
        "ejecutado tiene su evidencia en el capítulo siguiente y cada nivel que no se "
        "ejecutó aparece como planificado."
    )

    d.titulo("4.1 Objetivo", nivel=2)
    d.parrafo(
        "El objetivo es comprobar que FactuGest emite documentos electrónicos correctos "
        "en contenido, en cálculo y en identificación del emisor, que la interfaz de "
        "integración cumple el contrato que publica, y que las reglas de acceso y de "
        "registro de la actividad se aplican. Dicho de otro modo, no se busca demostrar "
        "que el sistema funciona sino encontrar aquello en lo que falla, que es la "
        f"diferencia entre probar y confirmar lo que uno ya cree ({narrativa('myers')})."
    )

    d.titulo("4.2 Alcance", nivel=2)
    d.parrafo(
        "Entra en el alcance todo lo que produce o modifica un documento electrónico y "
        "todo lo que decide quién puede hacerlo. En concreto, la aritmética tributaria "
        "con sus bases, descuentos y prorrateo del impuesto, la reserva del consecutivo "
        "autorizado, la generación de la representación gráfica y del archivo de "
        "intercambio, el contrato de entrada y de salida de la interfaz de integración, "
        "el control de acceso por rol, el registro de la actividad y el cálculo del "
        "consumo de cada cliente contra el cupo de su plan."
    )
    d.parrafo(
        "Queda fuera del alcance, y conviene decirlo antes de que alguien lo busque en el "
        "capítulo de resultados, la transmisión real ante la autoridad tributaria, que "
        f"depende de un proveedor tecnológico habilitado ({cita('dian42')}) con el que "
        "todavía no se ha formalizado el acuerdo. Queda fuera también el comportamiento "
        "del sistema bajo carga concurrente alta, porque no se ha ejecutado la prueba que "
        "lo mediría, y la verificación del despliegue en un servidor de producción, que "
        "todavía no existe."
    )
    d.parrafo(
        "La prioridad dentro del alcance no se repartió por igual. Sale del cruce del "
        "capítulo anterior, donde la característica con más requisitos resultó ser la "
        "seguridad, seguida por la eficiencia de desempeño, la fiabilidad y la "
        f"mantenibilidad ({cita('iso25010')}). A eso se suma un criterio de daño, pues "
        "lo que se prueba primero es aquello cuyo fallo produce un documento que no se "
        "puede corregir, como un número de resolución repetido, un impuesto mal calculado "
        "o una factura que dice haber sido expedida por quien no la expidió."
    )


def _estrategia(d):
    d.titulo("4.3 Estrategia y niveles de prueba", nivel=2)
    d.parrafo(
        "Se aplicaron cuatro niveles de prueba y cuatro tipos adicionales, con la "
        f"distinción habitual entre lo que se verifica en cada uno ({cita('istqb')}). La "
        "estrategia se apoya en dos decisiones que conviene explicar, porque determinan "
        "qué se automatizó y qué no."
    )
    d.parrafo(
        "La primera es que se automatiza lo que no necesita base de datos. La aritmética, "
        "las reglas de validación, el contrato de la interfaz, la generación del archivo "
        "de intercambio y el armado de la representación gráfica son funciones que reciben "
        "datos y devuelven un resultado, de modo que pueden probarse miles de veces en "
        "segundos y sirven de red permanente. Lo que exige base de datos y sesión de "
        "usuario se prueba de forma funcional, sobre el sistema en marcha, con registro en "
        "imagen del antes y el después."
    )
    d.parrafo(
        "La segunda es que el resultado esperado de una prueba se calcula a mano y no se "
        "copia de la salida del programa. Una prueba que repite lo que el código devolvió "
        "no verifica nada, porque queda en verde tanto si el código está bien como si "
        "está mal, y esa es una trampa fácil de caer cuando se escriben pruebas después "
        f"del código y no antes ({narrativa('beck')})."
    )
    d.tabla(
        "Niveles y tipos de prueba aplicados",
        ["Nivel o tipo", "Qué verifica", "Técnica", "Con qué se ejecuta", "Estado"],
        [[nivel, verifica, tecnica, herramienta, estado]
         for nivel, verifica, tecnica, herramienta, estado in NIVELES],
        nota=f"Clasificación de niveles según {cita('istqb')}. El estado corresponde a lo "
             "ocurrido hasta la fecha de este informe.",
        anchos=[2.4, 4.0, 3.0, 3.0, 2.4],
    )
    d.parrafo(
        f"El volumen resultante es de {TOTAL_UNITARIAS} pruebas automatizadas repartidas "
        f"en {len(UNITARIAS)} archivos, {len(INTEGRACION)} peticiones de prueba sobre la "
        f"interfaz de integración y {len(FUNCIONALES)} operaciones verificadas de forma "
        "funcional con registro en imagen. El detalle de cada grupo, con lo que protege y "
        "su resultado, está en el capítulo 5."
    )


def _entorno(d):
    d.titulo("4.4 Entorno y datos de prueba", nivel=2)
    d.parrafo(
        "Las pruebas se ejecutan en el entorno de desarrollo de cada integrante, que "
        "reproduce el del sistema completo. No hay todavía un servidor de pruebas "
        "separado, lo que se declara como riesgo más adelante."
    )
    d.tabla(
        "Entorno de ejecución de las pruebas",
        ["Componente", "Qué se usa"],
        [[componente, detalle] for componente, detalle in ENTORNO],
        nota=f"La batería automatizada se ejecuta con {HERRAMIENTA} y su corrida completa "
             f"tarda {DURACION}.",
        anchos=[4.6, 10.2],
    )
    d.parrafo(
        "Los datos merecen una explicación aparte, porque de ellos depende que una prueba "
        "signifique algo. El proyecto tiene un sembrador que crea la empresa emisora, el "
        "catálogo de servicios, catorce empresas suscritas con su llave y su plan, tres "
        "meses de documentos emitidos por cuenta de ellas y seis meses de ventas propias. "
        "Tiene tres propiedades pensadas para pruebas. Es determinista, de manera que dos "
        "siembras producen exactamente lo mismo y un resultado distinto señala un cambio "
        "en el sistema y no en los datos. Se verifica a sí mismo al terminar. Y sabe "
        "deshacer con exactitud lo que creó, de modo que la base queda como estaba."
    )
    d.parrafo(
        "Las pruebas automatizadas, en cambio, no usan el sembrador ni tocan la base de "
        "datos, y esa fue una decisión del plan. Una prueba que depende de una base "
        "depende también de su estado, del orden en que se ejecuta y de que la base esté "
        "levantada, con lo cual empieza a fallar por motivos que no tienen que ver con lo "
        "que pretende verificar. Las funciones que sí necesitan la base se verifican en el "
        "nivel funcional, con el sistema en marcha."
    )


def _criterios(d):
    d.titulo("4.5 Criterios de entrada y de salida", nivel=2)
    d.parrafo(
        "Una tarea entra a prueba cuando cumple estas condiciones."
    )
    d.vinetas([
        "El requisito que la origina está escrito en el catálogo del proyecto y tiene un "
        "medio de verificación declarado.",
        "El código está integrado en la rama de trabajo y el sistema levanta sin errores.",
        "Los datos necesarios existen, sea porque los crea el sembrador o porque la prueba "
        "los construye.",
    ])
    d.parrafo(
        "Y se considera probada cuando se cumplen todas las siguientes, que son las que "
        "cierran una tarea y permiten pasar a la que sigue."
    )
    d.vinetas([
        f"La batería completa de {TOTAL_UNITARIAS} pruebas automatizadas termina sin "
        "ninguna falla, y no solamente las pruebas del módulo que se tocó.",
        "Las peticiones de la interfaz de integración responden con el código y la forma "
        "que documenta el contrato, incluido el caso del error.",
        "La operación se ejecutó en el panel y quedó su registro en imagen, cuando se "
        "trata de una función de la aplicación web.",
        "No queda ningún defecto de severidad crítica abierto, y los de severidad mayor "
        "están registrados con su decisión.",
    ])


def _defectos(d):
    d.titulo("4.6 Gestión de los defectos", nivel=2)
    d.parrafo(
        "Un defecto encontrado sigue siempre el mismo recorrido, y el orden de los pasos "
        "importa. Primero se escribe una prueba que lo reproduce y que, por lo tanto, "
        "falla. Después se corrige el código hasta que esa prueba pasa. Y por último la "
        "prueba se queda en la batería, de modo que el defecto no puede volver sin que "
        "alguien se entere. Corregir primero y probar después deja la duda de si la "
        "prueba habría detectado el defecto original, que es precisamente lo que se "
        "necesita saber."
    )
    d.parrafo(
        "Los defectos se clasifican por lo que producen y no por lo que cuesta "
        "arreglarlos, porque lo que decide si una entrega se detiene es el daño y no el "
        "esfuerzo."
    )
    d.tabla(
        "Clasificación de los defectos por severidad",
        ["Severidad", "Qué la define", "Ejemplo encontrado en el proyecto"],
        [[severidad, definicion, ejemplo]
         for severidad, definicion, ejemplo in SEVERIDADES],
        nota="Los tres ejemplos son defectos reales encontrados durante la construcción y "
             "ya corregidos. Su detalle y la prueba que hoy los cubre están en el "
             "capítulo 5.",
        anchos=[2.2, 5.0, 7.6],
    )


def _riesgos(d):
    d.titulo("4.7 Riesgos del plan", nivel=2)
    d.parrafo(
        "Todo plan de pruebas tiene puntos ciegos, y declararlos es parte del plan. Los "
        "cinco siguientes son los de este, con lo que se hizo para reducirlos."
    )
    d.tabla(
        "Riesgos del plan de pruebas y su tratamiento",
        ["Riesgo", "Qué pasa si ocurre", "Cómo se atiende"],
        [[riesgo, efecto, mitigacion] for riesgo, efecto, mitigacion in RIESGOS],
        nota="Ninguno de los cinco está resuelto por completo. Los que dependen del "
             "despliegue se atienden en la fase correspondiente del proyecto.",
        anchos=[3.6, 5.2, 6.0],
    )
    d.parrafo(
        "El primero merece una nota, porque es el que más se subestima. Hay defectos que "
        "una prueba no puede encontrar en un entorno de un solo usuario, y el más caro de "
        "este sistema es el de dos peticiones simultáneas que leen el mismo consecutivo y "
        "emiten dos documentos con el mismo número de una resolución autorizada. Ese "
        "riesgo no se cubrió con una prueba sino por diseño, reservando el número en una "
        "sola sentencia y dejando además un índice único en la base que la propia base "
        "hace cumplir. Es la respuesta correcta, porque una prueba de concurrencia "
        "detecta el problema algunas veces, mientras que el índice lo impide siempre."
    )


def _roles(d):
    d.titulo("4.8 Roles y responsabilidades", nivel=2)
    d.parrafo(
        "El equipo es de tres personas, de modo que los roles no corresponden a "
        "integrantes distintos sino a funciones que cada uno asume según la tarea. La "
        "regla que sí se sostiene es que nadie ejecuta la prueba funcional de lo que él "
        "mismo escribió."
    )
    d.tabla(
        "Roles del plan de pruebas",
        ["Rol", "Responsabilidad"],
        [[rol, responsabilidad] for rol, responsabilidad in ROLES],
        nota="Los cuatro roles rotan entre los tres integrantes del equipo.",
        anchos=[4.4, 10.4],
    )
    d.parrafo(
        f"Como referencia del trabajo cubierto, el catálogo del proyecto tiene {len(RNF)} "
        "requisitos no funcionales con su medio de verificación declarado, y todos ellos "
        "quedaron clasificados en el capítulo anterior. La colección de peticiones de "
        f"prueba está publicada en el propio repositorio ({COLECCION}) y las imágenes de "
        f"las pruebas funcionales, en {CARPETA_CAPTURAS}."
    )
