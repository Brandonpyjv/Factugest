"""
AA1, capítulo 3. El referente de calidad adoptado y su cruce con el sistema.

Este es el capítulo que responde al criterio de evaluación de la guía, que no pide
conocer los modelos sino ajustar el proceso al referente adoptado. De ahí que lo que
más ocupa no sea la declaración del estándar, que son dos páginas, sino la matriz que
lo cruza contra los 32 requisitos no funcionales del sistema y contra la evidencia
que respalda cada uno.

La matriz se calcula, no se escribe. `MAPA` asigna a cada requisito su característica
y su subcaracterística, y las tablas se arman contando sobre esa asignación, de modo
que no pueda haber un requisito sin clasificar ni una cuenta que no cuadre con las
filas. La comprobación está al final del archivo y falla en la generación.
"""
from collections import defaultdict

from evidencia import RNF
from fuentes import cita, narrativa

CITADAS = ["iso25010", "iso9126", "iso9001", "iso15504", "iso12207", "cmmi",
           "portal25000", "scalone", "estayno", "dian42"]

# Las ocho características del modelo de calidad de producto, en el orden de la norma.
CARACTERISTICAS = [
    "Adecuación funcional",
    "Eficiencia de desempeño",
    "Compatibilidad",
    "Usabilidad",
    "Fiabilidad",
    "Seguridad",
    "Mantenibilidad",
    "Portabilidad",
]

# requisito: (característica, subcaracterística). Es la asignación que sostiene todo
# el capítulo, así que se escribe una sola vez y las tablas se derivan de ella.
MAPA = {
    "RNF 01": ("Eficiencia de desempeño", "Comportamiento temporal"),
    "RNF 02": ("Eficiencia de desempeño", "Comportamiento temporal"),
    "RNF 03": ("Eficiencia de desempeño", "Utilización de recursos"),
    "RNF 04": ("Seguridad", "Confidencialidad"),
    "RNF 05": ("Seguridad", "Confidencialidad"),
    "RNF 06": ("Seguridad", "Confidencialidad"),
    "RNF 07": ("Seguridad", "Autenticidad"),
    "RNF 08": ("Seguridad", "Autenticidad"),
    "RNF 09": ("Seguridad", "Confidencialidad e integridad"),
    "RNF 10": ("Seguridad", "Integridad"),
    "RNF 11": ("Fiabilidad", "Tolerancia a fallos"),
    "RNF 12": ("Adecuación funcional", "Corrección funcional"),
    "RNF 13": ("Adecuación funcional", "Corrección funcional"),
    "RNF 14": ("Seguridad", "Responsabilidad"),
    "RNF 15": ("Seguridad", "No repudio"),
    "RNF 16": ("Fiabilidad", "Tolerancia a fallos"),
    "RNF 17": ("Fiabilidad", "Disponibilidad"),
    "RNF 18": ("Usabilidad", "Capacidad de ser usado"),
    "RNF 19": ("Usabilidad", "Protección contra errores de usuario"),
    "RNF 20": ("Usabilidad", "Accesibilidad"),
    "RNF 21": ("Portabilidad", "Adaptabilidad"),
    "RNF 22": ("Compatibilidad", "Interoperabilidad"),
    "RNF 23": ("Compatibilidad", "Interoperabilidad"),
    "RNF 24": ("Adecuación funcional", "Corrección funcional"),
    "RNF 25": ("Fiabilidad", "Capacidad de recuperación"),
    "RNF 26": ("Mantenibilidad", "Modularidad y reusabilidad"),
    "RNF 27": ("Mantenibilidad", "Modularidad"),
    "RNF 28": ("Mantenibilidad", "Capacidad de ser modificado"),
    "RNF 29": ("Mantenibilidad", "Capacidad de ser probado"),
    "RNF 30": ("Eficiencia de desempeño", "Capacidad"),
    "RNF 31": ("Compatibilidad", "Interoperabilidad"),
    "RNF 32": ("Portabilidad", "Adaptabilidad e instalabilidad"),
}

# característica: (qué se le exige al sistema, con qué se comprueba hoy)
EVIDENCIA_POR_CARACTERISTICA = {
    "Adecuación funcional":
        ("Que el documento diga lo que debe decir, que el consumo se cuente de lo "
         "realmente emitido y que lo emitido para un tercero no aparezca como venta "
         "propia",
         "Las 35 pruebas de la aritmética tributaria y las 10 del membrete del PDF, más "
         "la separación en dos zonas de la base de datos"),
    "Eficiencia de desempeño":
        ("Que la emisión responda en menos de tres segundos, que el envío del correo no "
         "demore la respuesta y que los listados no traigan la tabla completa",
         "El correo agendado como tarea de fondo y las consultas paginadas del servicio "
         "de listados. La medición del tiempo bajo carga queda planificada"),
    "Compatibilidad":
        ("Que cualquier sistema pueda integrarse sin acuerdo previo y que un cambio no "
         "deje sin servicio a quien ya integró",
         "El contrato publicado en formato OpenAPI, la colección de 11 peticiones de "
         "prueba y la política de sacar una versión nueva antes que romper la vigente"),
    "Usabilidad":
        ("Que la navegación se agrupe por trabajo y no por tabla, que los errores señalen "
         "el campo que los provocó y que la interfaz sirva en cualquier pantalla",
         "Las 45 pruebas de las reglas de validación, que son las que producen el mensaje "
         "del formulario, y la encuesta aplicada a las empresas"),
    "Fiabilidad":
        ("Que una emisión a medias no deje rastro, que la caída de un servicio externo no "
         "impida facturar y que lo emitido se conserve",
         "La transacción que envuelve la emisión completa y el envío del correo fuera de "
         "esa transacción. El monitoreo de disponibilidad queda planificado"),
    "Seguridad":
        ("Que ninguna credencial se guarde legible, que cada ruta exija sesión, que dos "
         "documentos no compartan número y que quede constancia de quién hizo qué",
         "Las 11 pruebas del servicio de llaves, el registro de auditoría que solo se "
         "escribe, la reserva del consecutivo en una sola sentencia y el índice único "
         "por emisor, tipo y número"),
    "Mantenibilidad":
        ("Que la aritmética exista una sola vez, que las rutas no contengan lógica, que "
         "el esquema cambie por migraciones y que haya pruebas",
         "Las 190 pruebas automatizadas, la capa de servicios compartida por la "
         "aplicación web y la API, y el migrador que se puede ejecutar dos veces sin "
         "alterar nada la segunda"),
    "Portabilidad":
        ("Que el sistema se use desde cualquier equipo y navegador sin instalar nada",
         "La condición de aplicación web y la prueba en los navegadores de mayor uso"),
}

# (área de proceso del nivel 2, estado, con qué se sostiene)
CMMI_NIVEL2 = [
    ("Gestión de requisitos", "Cumplida",
     "82 requisitos funcionales y 32 no funcionales catalogados, trazados a 56 casos de "
     "uso y, los críticos, a pruebas automatizadas"),
    ("Planificación del proyecto", "Cumplida",
     "Trabajo por iteraciones bajo Scrum, con la pila de producto repartida en ocho "
     "sprints y un cronograma de quince actividades"),
    ("Seguimiento y control del proyecto", "Cumplida",
     "Cuaderno de trabajo con bitácora de decisiones por tarea, y el tablero de control "
     "del propio sistema para la operación"),
    ("Gestión de la configuración", "Cumplida",
     "Control de versiones sobre todo el código, migraciones de base de datos "
     "versionadas y registradas, y versionado explícito de la interfaz de integración"),
    ("Aseguramiento de la calidad del proceso y del producto", "Cumplida",
     "Batería de pruebas ejecutable por cualquiera del equipo, invariantes del sistema "
     "escritos y revisión del formato de los entregables por herramienta"),
    ("Medición y análisis", "Parcial",
     "Se mide el resultado de las pruebas y el consumo de los clientes, pero no hay "
     "todavía medición de tiempos de respuesta ni de densidad de defectos"),
    ("Gestión de acuerdos con proveedores", "Parcial",
     "El acuerdo con el proveedor tecnológico habilitado está identificado y el "
     "adaptador está construido, pero la relación no se ha formalizado"),
]

# (referente, qué aporta, por qué no se adoptó como principal)
DESCARTADOS = [
    ("Modelo de McCall",
     "La partición de la calidad en operación, revisión y transición del producto",
     "Varios de sus once factores no tienen métrica directa y terminan evaluándose con "
     "listas subjetivas. Su aporte ya está recogido, ordenado y ampliado en la norma "
     "vigente"),
    ("Modelo de Boehm",
     "La trazabilidad desde una característica general hasta la métrica que la mide",
     "Es la idea que los estándares ISO adoptaron después. Adoptarlo hoy significaría "
     "usar una versión anterior de lo mismo"),
    ("ISO/IEC 9126",
     "Las seis características que fundaron el vocabulario común de calidad de producto",
     "Fue reemplazada en 2011 por la norma ISO/IEC 25010. Declarar como referente una "
     "norma sustituida es un defecto que un evaluador señala de inmediato"),
    ("ISO/IEC 15504 SPICE",
     "Un marco de evaluación de procesos por niveles de capacidad, alineado con el ciclo "
     "de vida del software",
     "Exige una evaluación formal por perfiles de capacidad que este proyecto no va a "
     "ejecutar. Declararlo sin evaluarlo sería afirmar algo que no se puede demostrar"),
    ("ISO 9001",
     "El enfoque a procesos, el pensamiento basado en riesgos y la orientación al cliente",
     "Norma la gestión de una organización y no los atributos de un programa. FactuGest "
     "es un proyecto formativo sin sistema de gestión de la calidad certificable"),
]


def escribir(d):
    _adopcion(d)
    _matriz(d)
    _desajustes(d)
    _proceso(d)
    _descartados(d)


def _cuenta_por_caracteristica():
    cuenta = defaultdict(list)
    for requisito, (caracteristica, _) in MAPA.items():
        cuenta[caracteristica].append(requisito)
    return {c: sorted(cuenta[c]) for c in CARACTERISTICAS}


def _abrevia(codigos):
    """«RNF 01» a «01», que es como se lee una lista de códigos de la misma serie."""
    return ", ".join(c.split()[1] for c in codigos)


def _adopcion(d):
    d.titulo("3. El referente de calidad adoptado", nivel=1, nueva_pagina=True)
    d.parrafo(
        "De la revisión anterior se desprende que ningún referente cubre por sí solo lo "
        "que un proyecto necesita, porque los de producto no dicen nada sobre la forma de "
        "trabajar y los de proceso no dicen nada sobre los atributos del programa. "
        "FactuGest adopta en consecuencia dos referentes complementarios, la norma "
        "ISO/IEC 25010 para la calidad del producto y el modelo CMMI, en su nivel 2 de "
        "madurez, como referencia para el proceso."
    )

    d.titulo("3.1 Por qué la norma ISO/IEC 25010", nivel=2)
    d.parrafo(
        f"La norma ISO/IEC 25010 es la versión vigente del modelo de calidad de producto y "
        f"reemplaza a la norma ISO/IEC 9126 desde 2011 ({cita('iso25010')}). Sobre esa "
        "condición de estándar actual pesan tres razones propias del sistema que se "
        "construyó."
    )
    d.parrafo(
        "La primera es que la seguridad dejó de ser una subcaracterística escondida dentro "
        "de la funcionalidad y pasó a ser una característica propia con cinco "
        "subcaracterísticas, entre ellas el no repudio y la responsabilidad. En un sistema "
        "que emite documentos con efectos legales por cuenta de otros, poder decir quién "
        "emitió qué y cuándo no es una precaución técnica sino parte del producto, y bajo "
        "la norma anterior ese requisito no tenía dónde clasificarse."
    )
    d.parrafo(
        "La segunda es la aparición de la compatibilidad como característica, con la "
        "interoperabilidad dentro. El producto principal de FactuGest es una interfaz que "
        "consumen sistemas ajenos que nadie de este equipo escribió, de modo que la "
        "capacidad de intercambiar información con ellos no es un atributo secundario del "
        "sistema sino aquello por lo que el cliente paga."
    )
    d.parrafo(
        "La tercera es de método. La norma organiza la calidad en características y "
        "subcaracterísticas evaluables, lo que permite tomar los requisitos no funcionales "
        "que el proyecto ya había escrito y clasificarlos contra un referente externo, en "
        "lugar de inventar categorías propias que solo se pueden juzgar por dentro. Ese "
        "cruce es el que se presenta a continuación, y de él sale además el orden en que "
        "se priorizaron las pruebas."
    )


def _matriz(d):
    d.titulo("3.2 Los requisitos del sistema contra el modelo de calidad", nivel=2)
    por_caracteristica = _cuenta_por_caracteristica()
    d.parrafo(
        f"El catálogo de requisitos no funcionales de FactuGest tiene {len(RNF)} entradas, "
        "agrupadas por categorías que el equipo definió durante el análisis. Clasificarlas "
        "contra las ocho características de la norma permite comprobar dos cosas, si "
        "alguna característica del estándar quedó sin atender y si alguna categoría propia "
        "no encuentra lugar en el estándar. El resultado es que las ocho características "
        "están cubiertas, con un reparto que dice bastante sobre la naturaleza del sistema."
    )
    d.tabla(
        "Los requisitos no funcionales de FactuGest clasificados por característica de "
        "calidad",
        ["Característica", "Requisitos", "Qué se le exige al sistema", "Con qué se "
         "sostiene hoy"],
        [[caracteristica,
          _abrevia(por_caracteristica[caracteristica]),
          EVIDENCIA_POR_CARACTERISTICA[caracteristica][0],
          EVIDENCIA_POR_CARACTERISTICA[caracteristica][1]]
         for caracteristica in CARACTERISTICAS],
        nota=f"Las ocho características son las del modelo de calidad de producto de la "
             f"norma ISO/IEC 25010 ({cita('iso25010')}). Los códigos corresponden al "
             "catálogo de requisitos del entregable de requisitos funcionales y no "
             "funcionales del proyecto, donde consta el enunciado completo de cada uno y "
             "su medio de verificación.",
        anchos=[2.9, 2.1, 4.9, 4.9],
    )
    mayor = max(CARACTERISTICAS, key=lambda c: len(por_caracteristica[c]))
    d.parrafo(
        f"La característica con más requisitos es {mayor.lower()}, con "
        f"{len(por_caracteristica[mayor])} de {len(RNF)}, y el reparto no es casual. Un "
        "proveedor tecnológico custodia las credenciales con las que otros emiten, numera "
        "documentos dentro de un rango autorizado y responde por lo que se hizo con esas "
        "credenciales, así que la mayor parte de lo que se le exige al sistema cae en "
        "confidencialidad, integridad, autenticidad, responsabilidad y no repudio. En un "
        "sistema de gestión corriente ese peso estaría en usabilidad o en adecuación "
        "funcional."
    )
    d.tabla(
        "Trazabilidad de cada requisito no funcional a la norma ISO/IEC 25010",
        ["Requisito", "Categoría del catálogo", "Característica", "Subcaracterística"],
        [[codigo, categoria, MAPA[codigo][0], MAPA[codigo][1]]
         for codigo, categoria, _, _ in RNF],
        nota="El enunciado completo de cada requisito y su medio de verificación están en "
             "el entregable de requisitos del proyecto. Aquí interesa la correspondencia "
             "entre la categoría con la que se escribió y la característica del estándar "
             "que le corresponde.",
        anchos=[2.2, 4.2, 4.2, 4.0],
    )


def _desajustes(d):
    d.titulo("3.3 Donde el catálogo propio y el estándar no coinciden", nivel=2)
    d.parrafo(
        "El cruce dejó tres desajustes que conviene declarar, porque son justamente lo que "
        "aporta clasificar contra un referente externo en lugar de contra categorías "
        "propias."
    )
    d.vinetas([
        ("Trazabilidad",
         "No existe como característica en la norma. Los dos requisitos que el catálogo "
         "agrupaba ahí, el registro de auditoría con el nombre del usuario y la "
         "imposibilidad de modificar ese registro, corresponden a responsabilidad y a no "
         "repudio, que son subcaracterísticas de seguridad. La norma los clasifica mejor "
         "de lo que estaban, porque deja explícito que su valor no es informativo sino "
         "probatorio"),
        ("Escalabilidad",
         "Tampoco existe como característica, y sus dos requisitos se reparten. Admitir "
         "nuevas empresas emisoras sin tocar el código es capacidad, dentro de eficiencia "
         "de desempeño, mientras que publicar una versión nueva de la interfaz antes que "
         "romper la vigente es interoperabilidad, dentro de compatibilidad"),
        ("Compatibilidad de navegadores",
         "El catálogo lo puso bajo compatibilidad por el nombre, pero funcionar en "
         "cualquier navegador sin instalación es adaptabilidad, que pertenece a "
         "portabilidad. La compatibilidad de la norma se refiere a coexistir e "
         "intercambiar información con otros sistemas, que es lo que hace la interfaz de "
         "integración, no la interfaz de usuario"),
    ])
    d.parrafo(
        "Ninguno de los tres obliga a reescribir el catálogo, que se escribió para el "
        "equipo y cumple su función. Lo que muestran es que un referente externo obliga a "
        "nombrar las cosas con un vocabulario que otros también usan, y esa es "
        "precisamente la utilidad de adoptar un estándar en lugar de declarar principios "
        "propios."
    )


def _proceso(d):
    d.titulo("3.4 El referente de proceso, CMMI en su nivel 2", nivel=2)
    d.parrafo(
        f"En el proceso, el referente adoptado es CMMI ({cita('cmmi')}), y la elección del "
        "nivel 2 es deliberada. El nivel 2 describe una organización que planifica y "
        "controla su trabajo por proyecto, gestiona sus requisitos y su configuración, "
        "mide lo que hace y asegura la calidad del producto y del proceso, que es "
        "exactamente el alcance que un equipo de formación puede sostener y demostrar. "
        "Declarar un nivel superior obligaría a mostrar procesos definidos para toda una "
        "organización, que aquí no existe."
    )
    d.parrafo(
        "Conviene además una precisión que evita una afirmación falsa. Un nivel de madurez "
        "se obtiene mediante una evaluación formal realizada por personal acreditado, de "
        "modo que este proyecto no está en el nivel 2 en el sentido de la certificación. "
        "Lo que se sostiene es que las siete áreas de proceso de ese nivel se usaron como "
        "referencia y que cinco de ellas se cubren con evidencia verificable, mientras que "
        "dos se cubren de forma parcial."
    )
    d.tabla(
        "Las áreas de proceso del nivel 2 de CMMI frente al proyecto",
        ["Área de proceso", "Estado", "Con qué se sostiene"],
        [[area, estado, evidencia] for area, estado, evidencia in CMMI_NIVEL2],
        nota=f"Áreas de proceso según {cita('cmmi')}. El estado declarado como parcial "
             "corresponde a lo que existe pero no está completo, y no a lo que está "
             "planificado.",
        anchos=[4.4, 1.8, 8.6],
    )
    d.parrafo(
        "Las dos áreas parciales están declaradas como tales a propósito. En medición y "
        "análisis se mide el resultado de la batería de pruebas y el consumo de cada "
        "cliente, pero no hay todavía medición de tiempos de respuesta ni conteo de "
        "densidad de defectos, y eso es justamente lo que el plan de pruebas del capítulo "
        "siguiente deja como trabajo pendiente. En gestión de acuerdos con proveedores, la "
        "relación con el proveedor tecnológico habilitado ante la autoridad tributaria "
        "está identificada y el adaptador que la consumirá está construido y probado, pero "
        "el acuerdo no se ha formalizado, de modo que la transmisión real todavía no "
        "ocurre."
    )


def _descartados(d):
    d.titulo("3.5 Los referentes que no se adoptaron", nivel=2)
    d.parrafo(
        "Elegir un referente obliga a decir por qué no se eligieron los otros, y en varios "
        "casos el motivo no es que sean peores sino que ya están recogidos en el que se "
        "adoptó."
    )
    d.tabla(
        "Referentes revisados y no adoptados como principales",
        ["Referente", "Qué aporta", "Por qué no se adoptó"],
        [[referente, aporte, motivo] for referente, aporte, motivo in DESCARTADOS],
        nota=f"La revisión de cada uno está en el capítulo 2. Las normas ISO/IEC 15504 e "
             f"ISO 9001 se citan según {cita('iso15504')} e {cita('iso9001')}.",
        anchos=[3.4, 5.4, 6.0],
    )
    d.parrafo(
        f"Queda una precisión sobre la norma ISO/IEC 15504. Que no se adopte como marco de "
        f"evaluación no significa que su contenido sea ajeno al proyecto, pues está "
        f"alineada con la norma ISO/IEC 12207 sobre los procesos del ciclo de vida "
        f"({cita('iso12207')}), y varios de esos procesos, como la verificación y la "
        "gestión de la configuración, son los mismos que el nivel 2 de CMMI pide y que el "
        "proyecto sí aplica. La diferencia está en el instrumento, no en el fondo, y "
        f"{narrativa('scalone')} ya señalaba que los referentes de proceso comparten buena "
        "parte de sus prácticas y se distinguen sobre todo por la forma de evaluarlas."
    )


def _comprobar():
    """Que no haya requisitos sin clasificar ni clasificados que no existan.

    Va aquí y no en las pruebas del sistema porque protege este documento, no el
    software: si alguien agrega un requisito al catálogo del proyecto y no lo
    clasifica, la matriz saldría con una fila menos y nadie lo notaría leyendo.
    """
    catalogo = {codigo for codigo, _, _, _ in RNF}
    sin_clasificar = catalogo - set(MAPA)
    inventados = set(MAPA) - catalogo
    assert not sin_clasificar, f"Requisitos sin característica: {sorted(sin_clasificar)}"
    assert not inventados, f"Clasificados y no existentes: {sorted(inventados)}"
    desconocidas = {c for c, _ in MAPA.values()} - set(CARACTERISTICAS)
    assert not desconocidas, f"Características fuera de la norma: {sorted(desconocidas)}"
    vacias = set(CARACTERISTICAS) - {c for c, _ in MAPA.values()}
    assert not vacias, f"Características sin ningún requisito: {sorted(vacias)}"


_comprobar()
