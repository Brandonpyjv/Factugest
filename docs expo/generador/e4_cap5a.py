"""
E4 — Capítulo 5, parte A. Diseño de la solución: actores, casos de uso, diagrama
conceptual, diagrama estructural y mockups.

Los actores y la ficha de caso de uso se **importan** de los documentos de casos de
uso (E2 y E3). En el documento de grado no van los 56 casos ni las 17 fichas: van
el diagrama general, dos diagramas de módulo y una ficha completa como muestra del
formato, y el resto queda en los documentos anexos.

**Sobre el diagrama estructural.** La plantilla de referencia presenta en ese punto
el mismo diagrama de casos de uso del punto anterior, con las relaciones de
inclusión dibujadas. Aquí se presenta en su lugar la arquitectura por capas del
sistema, que es lo que el término designa en un capítulo de diseño y lo que hace
falta para entender el capítulo 6. Repetir el diagrama anterior con una variación
no habría agregado información.
"""
from pathlib import Path

import casos_de_uso as catalogo
from e2_diagramas import ACTORES
from e3_documentacion import DETALLE, _alternos, _pasos, _viñetas

BASE = Path(__file__).resolve().parent.parent
DIAGRAMAS = BASE / "entregables" / "diagramas"
MOCKUPS = BASE / "documento para que te guies claude"


def escribir(d):
    d.titulo("Capítulo 5. Diseño de la solución y arquitectura del sistema", nivel=1,
             nueva_pagina=True)
    _actores(d)
    _casos_de_uso(d)
    _conceptual(d)
    _estructural(d)
    _mockups(d)


def _actores(d):
    d.titulo("5.1 Actores", nivel=2)
    d.parrafo(
        "Un actor es un rol que interactúa con el sistema, no una persona en particular. La "
        "misma persona puede ejercer dos roles y un mismo rol puede corresponder a varias "
        "personas; lo que el diseño necesita saber es qué espera cada rol del sistema y hasta "
        "dónde alcanza."
    )
    d.parrafo(
        "El sistema reconoce seis actores. Cuatro corresponden a los roles del panel y se "
        "ordenan jerárquicamente, de modo que el alcance de cada uno contiene al del "
        "inferior. Los otros dos no son personas que operen el sistema, ya que uno es el "
        "sistema "
        "externo que consume la API, y es el que origina la mayor parte de la operación, y el "
        "otro es quien recibe el documento emitido."
    )
    d.tabla(
        "Actores del sistema y su alcance",
        ["Actor", "Descripción y alcance"],
        [[a, desc] for a, desc in ACTORES],
        nota="Elaboración propia.",
        anchos=[3.4, 12.9],
    )
    d.parrafo(
        "La inclusión del sistema cliente como actor es la que distingue este diseño del de un "
        "sistema de facturación convencional. En aquel, todos los actores son personas que "
        "diligencian formularios; aquí, el actor que más documentos origina es un programa "
        "que nunca ve una pantalla. Esa diferencia obliga a que la emisión esté disponible "
        "como operación de una interfaz y no solo como formulario, y es la razón por la que "
        "la lógica de negocio no puede residir en las rutas de la aplicación web."
    )


def _casos_de_uso(d):
    d.titulo("5.2 Diagrama de casos de uso", nivel=2, nueva_pagina=True)
    d.parrafo(
        f"El análisis identificó {len(catalogo.todos())} casos de uso, agrupados en los ocho "
        "módulos funcionales del sistema. Un caso de uso describe un objetivo que un actor "
        "persigue y el resultado observable que obtiene; no describe una pantalla ni una "
        "operación sobre la base de datos, razón por la cual su número no coincide con el de "
        "los requisitos funcionales, porque un caso como «gestionar impuestos» cubre el "
        "registro, la "
        "consulta, la actualización y la eliminación, que para quien usa el sistema son un "
        "mismo propósito."
    )
    d.parrafo(
        "Se presentan a continuación el diagrama general y dos diagramas de módulo. El "
        "conjunto completo de los nueve diagramas y la documentación de cada caso constan en "
        "los documentos anexos."
    )
    d.figura(
        "Diagrama general de casos de uso de FactuGest",
        DIAGRAMAS / "DCU-00 general.png",
        nota="Elaboración propia. Cada elipse agrupa los casos de uso de un módulo. El "
             "comprador aparece recibiendo un documento sin iniciar ningún caso, lo que "
             "corresponde a su situación real, ya que es el destinatario de la operación y no tiene "
             "acceso al sistema.",
    )
    d.parrafo(
        "El diagrama del módulo de documentos electrónicos concentra el propósito del "
        "sistema. Los tres casos de emisión, que son factura, nota crédito y nota débito, "
        "comparten "
        "los pasos que hacen válido a un documento, que por eso se modelan como casos "
        "incluidos y no se repiten en cada uno, y son reservar el consecutivo, calcular los "
        "totales "
        "y generar los dos archivos."
    )
    d.figura(
        "Diagrama de casos de uso del módulo de gestión de documentos electrónicos",
        DIAGRAMAS / "DCU-02 Gestión de documentos electrónicos.png",
        nota="Elaboración propia. El envío del documento al comprador se modela como "
             "extensión y no como inclusión, porque el documento queda emitido y es válido aunque "
             "el "
             "correo no salga. Modelarlo al revés supondría que un servidor de correo caído "
             "impide facturar.",
    )
    d.figura(
        "Diagrama de casos de uso del módulo de integración mediante API REST",
        DIAGRAMAS / "DCU-08 Integración mediante API REST.png",
        nota="Elaboración propia. Presenta el sistema desde la perspectiva del integrador. La "
             "autenticación por llave está incluida en todas las operaciones.",
    )

    d.titulo("5.2.1 Documentación de un caso de uso", nivel=3, nueva_pagina=True)
    d.parrafo(
        "Cada caso de uso cuenta con su documentación, que establece con qué condiciones "
        "empieza, qué pasos recorre, qué caminos alternos admite, en qué estado deja al "
        "sistema y qué ocurre cuando algo falla. Se presenta como muestra la ficha del caso "
        "central del sistema; las diecisiete fichas de los casos críticos y el formato breve "
        "de los restantes constan en el documento anexo."
    )
    _ficha(d, "CU-08")
    d.parrafo(
        "El orden de los pasos de esta ficha no es una descripción del código sino una "
        "exigencia del negocio. La validación del cupo ocurre en el paso 3, antes de reservar "
        "el consecutivo en el paso 4, porque la numeración de una resolución es un recurso "
        "autorizado y finito, y rechazar una emisión después de haber tomado un número gastaría "
        "un consecutivo en un documento que nunca existió."
    )


def _ficha(d, codigo):
    catalogo_completo = {c[0]: c for c in catalogo.todos()}
    _, nombre, modulo, actores, descripcion, rf = catalogo_completo[codigo]
    precondiciones, flujo, alternos, postcondiciones, excepciones = DETALLE[codigo]
    d.tabla(
        f"Ficha del caso de uso {codigo}, emitir factura de venta",
        ["CASO DE USO", f"{codigo}. {nombre}"],
        [
            ["Módulo", modulo],
            ["Actores", ", ".join(actores)],
            ["Requisitos que cubre", rf],
            ["Descripción", descripcion],
            ["Precondiciones", _viñetas(precondiciones)],
            ["Secuencia normal", _pasos(flujo)],
            ["Flujos alternos", _alternos(alternos)],
            ["Postcondiciones", _viñetas(postcondiciones)],
            ["Excepciones", _viñetas(excepciones)],
        ],
        nota="Elaboración propia.",
        anchos=[3.6, 12.7],
    )


def _conceptual(d):
    d.titulo("5.3 Diagrama conceptual", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El diagrama conceptual presenta el sistema completo organizado en los ocho paquetes "
        "que corresponden a sus módulos funcionales, con las operaciones principales de cada "
        "uno y los actores que las utilizan. Su propósito es ofrecer, en una sola vista, el "
        "alcance de la solución antes de entrar en el detalle de su construcción."
    )
    d.figura(
        "Diagrama conceptual del sistema",
        DIAGRAMAS / "FIG-conceptual.png",
        nota="Elaboración propia. Se relacionan las operaciones principales de cada módulo; "
             "el detalle completo consta en los diagramas de casos de uso.",
    )
    d.parrafo(
        "La distribución de los actores frente a los paquetes revela una característica del "
        "sistema que conviene señalar. El administrador alcanza siete de los ocho módulos, "
        "mientras que el sistema cliente alcanza dos, el de documentos electrónicos y el de "
        "integración. Esa asimetría no es un desequilibrio del diseño, sino la consecuencia de "
        "que la plataforma tenga dos naturalezas a la vez, ya que es una herramienta de "
        "administración para quien presta el servicio y una interfaz de emisión para quien lo "
        "consume."
    )


def _estructural(d):
    d.titulo("5.4 Diagrama estructural", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El diagrama estructural presenta la organización interna del sistema en capas con "
        "responsabilidades separadas. La capa de presentación reúne las dos formas de acceder "
        "a la plataforma; la de rutas recibe las peticiones y las traduce; la de lógica de "
        "negocio concentra las reglas; y la de datos almacena la información en las dos zonas "
        "que la base mantiene separadas."
    )
    d.figura(
        "Arquitectura por capas del sistema",
        DIAGRAMAS / "FIG-estructural.png",
        nota="Elaboración propia. Las flechas indican la dirección de la dependencia, de modo "
             "que una capa "
             "conoce a la que está debajo y no al contrario.",
    )
    d.parrafo(
        "La decisión que define esta arquitectura está en el punto donde las dos entradas "
        "convergen. Tanto las rutas de la aplicación web como las de la interfaz de "
        "integración llaman a la misma capa de servicios, de modo que una regla tributaria se "
        "implementa una sola vez y rige por igual para ambas. La alternativa, que cada "
        "entrada resolviera su propio cálculo, habría producido, tarde o temprano, dos "
        "resultados distintos para la misma operación, pues una factura emitida desde el "
        "formulario "
        "y otra emitida por la API con los mismos datos habrían podido diferir en el impuesto."
    )
    d.parrafo(
        "De esa separación se sigue una regla que el proyecto mantuvo durante toda la "
        "construcción, y es que las rutas se limitan a recibir y responder, y no contienen "
        "lógica de "
        "negocio. Comprobar que se cumple es sencillo, ya que una regla que aparezca escrita "
        "dentro "
        "de una ruta es una regla que la otra entrada no tiene, y esa comprobación se hizo "
        "parte de la revisión de cada sprint."
    )
    d.parrafo(
        "La capa de datos aparece dividida en dos zonas y un puente. La zona comercial guarda "
        "lo que el proveedor vende, esto es, sus planes, sus clientes y sus facturas. La zona de "
        "middleware guarda lo que el proveedor emite por cuenta de terceros. La separación no "
        "es una preferencia de organización, porque el tablero y los reportes leen la zona "
        "comercial, "
        "de manera que un documento emitido para una empresa cliente, si se guardara allí, "
        "aparecería contabilizado como ingreso propio del proveedor. El puente registra qué "
        "mes de qué cliente ya fue cobrado, y es el único lugar donde las dos zonas se tocan."
    )


def _mockups(d):
    d.titulo("5.5 Mockups del sistema", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Antes de construir las pantallas se elaboraron mockups de las dos más utilizadas, el "
        "panel de control, que es la primera vista al ingresar al sistema, y el formulario de "
        "creación de facturas, que es donde se concentra la operación diaria. Diseñar estas "
        "dos pantallas por adelantado permitió resolver sobre el papel decisiones de "
        "disposición que habría sido costoso cambiar una vez construidas."
    )
    d.figura(
        "Mockup del panel de control",
        MOCKUPS / "Mockup panel de control.png",
        nota="Elaboración propia. Propuesta de disposición de los indicadores del servicio y "
             "de la venta, con los filtros de periodo en la parte superior.",
    )
    d.parrafo(
        "El mockup del panel resolvió una pregunta de fondo antes de escribir código, y era qué "
        "debía mostrarse primero. La decisión fue separar el tablero en dos secciones y "
        "ordenarlas de manera que el servicio prestado aparezca antes que su cobro, porque es "
        "lo que la empresa hace; cobrarlo viene después. Un tablero que abriera con las cifras "
        "de venta habría descrito a un comercio y no a un proveedor de facturación."
    )
    d.figura(
        "Mockup del formulario de creación de factura",
        MOCKUPS / "Mockup crear nueva factura.png",
        nota="Elaboración propia. Propuesta de organización del formulario en pasos, con el "
             "resumen de totales visible de forma permanente.",
    )
    d.parrafo(
        "El mockup del formulario incorporó un hallazgo de la observación directa, y es que el "
        "registro "
        "de una venta toma pocos segundos, de modo que cualquier pantalla que agregue pasos "
        "será rechazada por quien la usa. De ahí que el formulario se organizara en tres "
        "momentos, que son a quién se le factura, qué se le factura y cómo paga, con el resumen de "
        "totales siempre a la vista, en lugar de repartir la información en pantallas "
        "sucesivas que obliguen a avanzar y retroceder para verificar una cifra."
    )
