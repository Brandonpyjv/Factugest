"""
AA1, capítulo 5. Las pruebas ejecutadas.

Es el capítulo de evidencia, así que todo lo que aparece aquí es comprobable. Los
casos de la tabla no son ejemplos redactados para el informe: son las pruebas de la
batería del proyecto, con sus valores de entrada y sus resultados esperados tal como
están escritos en los archivos, y la corrida completa que los respalda va como anexo.

Los importes se escriben con separador de miles y coma decimal, que es como los
muestra el sistema, aunque en el código estén como números.
"""
from comun import RAIZ
from evidencia import (DURACION, FECHA_CORRIDA, FUNCIONALES, HERRAMIENTA, INTEGRACION,
                       TOTAL_UNITARIAS, UNITARIAS)
from fuentes import cita

CITADAS = ["istqb", "myers", "iso25010", "dian42"]

CAPTURAS = RAIZ / "docs expo" / "documento para que te guies claude"

# (caso, qué verifica, entrada, resultado esperado, resultado obtenido)
# Todos salen de pruebas reales. El estado es «Superada» en los quince, así que no
# se repite en una columna que diría siempre lo mismo.
CASOS = [
    ("CP-01", "El cálculo de una línea con impuesto",
     "2 unidades a 189.000 con tarifa del 19 %",
     "Bruto de 378.000 e impuesto de 71.820",
     "Bruto de 378.000 e impuesto de 71.820"),
    ("CP-02", "El descuento propio de una línea",
     "2 unidades a 189.000, con 5 % de descuento y tarifa del 19 %",
     "Descuento de 18.900, base de 359.100 e impuesto de 68.229",
     "Descuento de 18.900, base de 359.100 e impuesto de 68.229"),
    ("CP-03", "Que una línea exenta no genere impuesto",
     "3 unidades a 12.000 con tarifa del 0 %",
     "Base de 36.000 e impuesto de 0",
     "Base de 36.000 e impuesto de 0"),
    ("CP-04", "Un documento con tarifas distintas en sus líneas",
     "Tres líneas, al 19 %, al 5 % con 10 % de descuento y al 0 %",
     "Bruto de 162.000, descuentos de 3.000, base de 159.000, impuestos de 20.350 y "
     "total de 179.350",
     "Los cinco valores coinciden"),
    ("CP-05", "El prorrateo del impuesto sobre el descuento de factura",
     "Una línea de 100.000 al 19 % con descuento de factura de 10.000",
     "Base de 90.000 e impuesto de 17.100, y no los 19.000 de la base sin descuento",
     "Base de 90.000 e impuesto de 17.100"),
    ("CP-06", "El prorrateo cuando el documento tiene varias tarifas",
     "Las tres líneas de CP-04 con descuento de factura de 9.000",
     "Descuentos de 12.000, base de 150.000, impuestos de 19.198,11 y total de "
     "169.198,11",
     "Los cuatro valores coinciden"),
    ("CP-07", "Que una nota crédito de anulación devuelva lo facturado",
     "Factura de tres teclados con 10 % de descuento y un ratón, todo al 19 %",
     "La nota repite la base, los impuestos y el total de la factura, y su mismo "
     "número de líneas",
     "Los tres importes y el número de líneas coinciden"),
    ("CP-08", "Que una devolución parcial prorratee base, descuento e impuesto",
     "Devolución de una unidad de las tres de la primera línea",
     "Bruto de 100.000, descuento de 10.000, base de 90.000, impuesto de 17.100 y "
     "total de 107.100, que es un tercio exacto",
     "Los cinco valores coinciden"),
    ("CP-09", "El dígito de verificación del NIT según el algoritmo de la autoridad",
     "Los NIT 890903938, 800197268 y 900373115",
     "Los dígitos 8, 4 y 3 respectivamente",
     "Los tres dígitos coinciden"),
    ("CP-10", "Que la identificación se valide según su tipo de documento",
     "El valor AB1234 como cédula y el valor AV123456 como pasaporte",
     "La cédula se rechaza indicando que solo admite números, y el pasaporte se "
     "acepta",
     "El rechazo y la aceptación se producen"),
    ("CP-11", "El excedente sobre el cupo del plan",
     "418 documentos emitidos contra un cupo de 400, y 400 contra 400",
     "Excedente de 18 en el primer caso y de 0 en el segundo, con el aviso encendido",
     "Excedente de 18 y de 0, con el aviso encendido"),
    ("CP-12", "Las propiedades de la llave de la interfaz de integración",
     "Cincuenta llaves generadas de forma consecutiva",
     "Prefijo de veinte caracteres como máximo, secreto de treinta como mínimo, "
     "ninguna llave repetida y un resumen que no permite recuperar el secreto",
     "Las cuatro propiedades se cumplen"),
    ("CP-13", "Que el membrete del documento sea el de la empresa que emite",
     "Documento de una clínica generado con su emisor",
     "El texto del documento no contiene en ninguna parte el nombre del proveedor "
     "tecnológico",
     "El nombre del proveedor no aparece"),
    ("CP-14", "El rechazo de un documento cuyo total no cuadra",
     "Cabecera con un total de 999.999 que no corresponde a su base más sus impuestos",
     "Rechazo explicando la inconsistencia, devuelto como respuesta y no como error "
     "del programa",
     "Rechazo con el mensaje esperado y sin excepción"),
    ("CP-15", "Que emitir dos veces la misma venta no gaste dos números",
     "La misma petición de emisión enviada por segunda vez con su misma referencia",
     "La segunda responde con el documento que ya existía y no crea uno nuevo",
     "Devuelve el documento existente"),
]

# (petición, código esperado, qué se comprueba en la respuesta)
RESPUESTAS = {
    1: ("200", "El emisor con el que numera quien integra"),
    2: ("201", "El número, el código único y los enlaces a los dos archivos"),
    3: ("200", "El mismo documento de la primera emisión, sin número nuevo"),
    4: ("200", "El estado actual del documento y si una nota lo anuló"),
    5: ("200", "Un archivo PDF"),
    6: ("200", "El archivo de intercambio en el estándar UBL 2.1"),
    7: ("200", "El listado paginado con la referencia con la que se envió cada uno"),
    8: ("201", "La nota con los importes de la factura original"),
    9: ("201", "La parte proporcional de base, descuento e impuesto"),
    10: ("201", "El adicional con el impuesto descompuesto o sumado, según se pida"),
    11: ("401", "La forma común de los errores, con su código y su mensaje"),
}

# (qué se verificó, cómo, resultado)
SEGURIDAD = [
    ("Que ninguna contraseña quede legible",
     "Inspección de la tabla de usuarios después de crear una cuenta",
     "Solo consta el resumen calculado con el algoritmo de cifrado en un sentido"),
    ("Que del secreto de una llave solo se guarde su resumen",
     "Inspección de la tabla de clientes y las pruebas del servicio de llaves",
     "En claro solo queda el prefijo, que sirve para localizar la fila"),
    ("Que toda ruta del panel exija sesión",
     "Petición a una ruta protegida sin haber iniciado sesión",
     "Redirección al formulario de ingreso"),
    ("Que el acceso se limite por rol",
     "Ingreso con una cuenta de cajero a las rutas reservadas",
     "Bloqueo de los módulos de la plataforma, los reportes y la configuración"),
    ("Que la sesión se cierre por inactividad y no por tiempo transcurrido",
     "Uso continuo frente a inactividad prolongada durante el mismo lapso",
     "El uso continuo no corta la sesión y la inactividad sí"),
    ("Que una llave inválida y una suspendida se distingan",
     "Peticiones con una llave mal formada y con una de un cliente suspendido",
     "Respuesta 401 en el primer caso y 403 en el segundo"),
    ("Que no entren credenciales al registro de actividad",
     "Rotación de una llave y revisión del registro",
     "Consta el hecho de la rotación y no la llave"),
]


def escribir(d):
    _resumen(d)
    _casos(d)
    _integracion(d)
    _funcionales(d)
    _seguridad(d)
    _usabilidad(d)


def _resumen(d):
    d.titulo("5. Pruebas ejecutadas", nivel=1, nueva_pagina=True)
    d.parrafo(
        f"Este capítulo presenta lo que se ejecutó y su resultado. La batería "
        f"automatizada se corrió por última vez el {FECHA_CORRIDA} con {HERRAMIENTA}, y "
        f"sus {TOTAL_UNITARIAS} pruebas terminaron sin ninguna falla en {DURACION}. La "
        "salida completa de esa corrida va como anexo al final del informe, de modo que "
        "las cifras que siguen no dependen de que el lector confíe en el texto."
    )

    d.titulo("5.1 Pruebas unitarias", nivel=2)
    d.parrafo(
        "Las pruebas unitarias cubren lo que se puede verificar sin base de datos ni "
        "servidor, que en este sistema es justamente donde vive el riesgo mayor, pues "
        "ahí están la aritmética con la que se calcula un impuesto, las reglas con las "
        "que se acepta o se rechaza un dato y el armado de los dos archivos que "
        "constituyen el documento electrónico."
    )
    d.tabla(
        "Reparto de las pruebas unitarias por lo que protegen",
        ["Archivo de pruebas", "Pruebas", "Qué protege"],
        [[archivo, str(cantidad), protege] for archivo, cantidad, protege in UNITARIAS],
        nota=f"Total de {TOTAL_UNITARIAS} pruebas en {len(UNITARIAS)} archivos. La "
             "cantidad sale de la corrida y no de contar funciones, porque una prueba "
             "escrita una vez y ejecutada con varios juegos de datos cuenta por cada "
             "juego.",
        anchos=[4.6, 1.6, 8.6],
    )
    d.parrafo(
        "El reparto no es proporcional al tamaño del código sino al daño que produce un "
        "error. Las reglas de validación y la aritmética tributaria concentran la mayor "
        "parte porque un dato mal aceptado o un impuesto mal calculado terminan impresos "
        f"en un documento con efectos legales ({cita('dian42')}), mientras que un error "
        "en una pantalla de consulta se corrige recargando la página."
    )


def _casos(d):
    d.titulo("5.2 Casos de prueba y sus resultados", nivel=2)
    d.parrafo(
        "La tabla siguiente detalla quince casos representativos de los distintos grupos. "
        "No son ejemplos redactados para este informe, sino pruebas de la batería con sus "
        "valores tal como están escritos, y por eso los importes son los que son y no "
        "cifras redondas. Los quince resultaron superados, que es lo esperable de una "
        "batería que se ejecuta a diario, y su valor no está en el estado sino en lo que "
        "cada uno impide que vuelva a pasar."
    )
    ancho = d.seccion_horizontal()
    d.tabla(
        "Casos de prueba representativos y sus resultados",
        ["Caso", "Qué verifica", "Entrada", "Resultado esperado", "Resultado obtenido"],
        [[caso, verifica, entrada, esperado, obtenido]
         for caso, verifica, entrada, esperado, obtenido in CASOS],
        nota="Los quince casos quedaron superados. Los valores esperados están calculados "
             "a mano en la propia prueba y no copiados de la salida del programa, que es "
             "la única forma de que una prueba distinga un cálculo correcto de uno que "
             "solo es consistente consigo mismo.",
        anchos=[1.8, 4.6, 5.2, 5.6, 5.0],
    )
    d.seccion_vertical()
    d.parrafo(
        "Tres casos merecen un comentario. El CP-05 y el CP-06 verifican el prorrateo del "
        "impuesto cuando la factura lleva un descuento global, que es el punto donde más "
        "fácil se equivoca un facturador, porque calcular el impuesto sobre la base sin "
        "descontar produce un documento que cobra de más y calcularlo aparte por línea "
        "produce diferencias de redondeo que no cuadran con el total. El CP-08 comprueba "
        "que una devolución parcial reparta también el descuento, ya que devolver la base "
        "completa de una línea que se vendió con rebaja significa regresar más dinero del "
        "que se recibió."
    )


def _integracion(d):
    d.titulo("5.3 Pruebas de integración sobre la interfaz", nivel=2)
    d.parrafo(
        f"La interfaz de integración se probó con una colección de {len(INTEGRACION)} "
        "peticiones que recorre el ciclo completo de una integración, en el mismo orden "
        "en que lo haría el sistema de un cliente. La colección está publicada en el "
        "repositorio del proyecto y sirve a la vez de prueba y de documentación para "
        "quien vaya a integrarse, de modo que no es un material escrito para el informe."
    )
    d.tabla(
        "Recorrido de las pruebas sobre la interfaz de integración",
        ["N.º", "Petición", "Método y ruta", "Respuesta esperada", "Qué se comprueba"],
        [[str(numero), nombre, f"{metodo} {ruta}", RESPUESTAS[numero][0],
          RESPUESTAS[numero][1]]
         for numero, nombre, metodo, ruta, _ in INTEGRACION],
        nota="Las once respondieron con el código y la forma esperados. La petición 3 es "
             "la que comprueba que repetir una emisión no gasta un segundo número de la "
             "resolución, y la 11 provoca un error a propósito para verificar que todos "
             "salen con la misma forma.",
        anchos=[0.9, 3.6, 3.8, 2.1, 4.4],
    )
    d.parrafo(
        "La petición número 3 es la más importante de la colección y conviene explicar "
        "por qué. Un sistema que integra puede perder la respuesta de una emisión por un "
        "corte de red y volver a enviarla, y si esa segunda petición emitiera otro "
        "documento, el cliente habría gastado dos números de una resolución autorizada "
        "para una sola venta. La prueba envía dos veces la misma petición y verifica que "
        "la segunda devuelva el documento que ya existía."
    )


def _funcionales(d):
    d.titulo("5.4 Pruebas funcionales", nivel=2)
    d.parrafo(
        f"Las operaciones que necesitan base de datos y sesión se verificaron sobre el "
        f"sistema en marcha, ejecutando la operación completa desde el navegador y "
        f"dejando registro del formulario diligenciado y del resultado. Se cubrieron "
        f"{len(FUNCIONALES)} operaciones, cada una con su par de imágenes."
    )
    d.tabla(
        "Operaciones verificadas de forma funcional",
        ["Operación", "Qué se comprueba", "Resultado"],
        [["Registrar un servicio del catálogo",
          "Que el servicio quede disponible para facturarse",
          "El servicio aparece en el catálogo y puede seleccionarse en una factura"],
         ["Registrar un cliente",
          "Que se validen la identificación y la ubicación contra los catálogos",
          "El cliente queda registrado con su municipio y su departamento"],
         ["Emitir una factura",
          "Que la factura tome el consecutivo, calcule los totales y genere sus archivos",
          "La factura queda emitida con su número, su código único y su representación "
          "gráfica"],
         ["Registrar un usuario",
          "Que la cuenta quede creada con su rol y su contraseña cifrada",
          "El usuario puede ingresar y ve solo lo que su rol permite"]],
        nota="Cada operación se registró en dos imágenes, el formulario diligenciado y el "
             "resultado. Las ocho imágenes están en el repositorio del proyecto.",
        anchos=[3.6, 5.4, 5.8],
    )
    d.figura(
        "Formulario de emisión de una factura, diligenciado antes de emitir",
        CAPTURAS / "registro de nueva factura.png",
        nota="La operación se ejecuta con el sistema en marcha y sobre la base de datos "
             "real, que es lo que distingue una prueba funcional de una unitaria.",
    )
    d.figura(
        "Resultado de la emisión, con la factura ya registrada",
        CAPTURAS / "registro de nueva factura emitida.png",
        nota="El documento queda con su número tomado del consecutivo autorizado, sus "
             "totales calculados y sus archivos generados.",
    )


def _seguridad(d):
    d.titulo("5.5 Pruebas de seguridad", nivel=2)
    d.parrafo(
        "La seguridad es la característica con más requisitos del sistema, según el cruce "
        f"del capítulo 3 ({cita('iso25010')}), de modo que se verificó punto por punto. "
        "Lo que sigue es lo comprobado, que corresponde a inspección y prueba dirigida y "
        "no a un análisis con herramienta especializada, el cual queda planificado en el "
        "capítulo siguiente."
    )
    d.tabla(
        "Verificaciones de seguridad ejecutadas",
        ["Qué se verificó", "Cómo", "Resultado"],
        [[que, como, resultado] for que, como, resultado in SEGURIDAD],
        nota="La distinción entre la respuesta 401 y la 403 no es un detalle técnico, "
             "pues en la primera quien integra revisa su configuración y en la segunda "
             "tiene que comunicarse con el proveedor.",
        anchos=[4.4, 4.6, 5.8],
    )


def _usabilidad(d):
    d.titulo("5.6 Pruebas de usabilidad", nivel=2)
    d.parrafo(
        "La usabilidad se verificó con dos técnicas distintas y en dos momentos. Durante "
        "el análisis se aplicó una encuesta a empresas de la ciudad para conocer cómo "
        "facturaban y qué dificultades tenían, y esa información orientó decisiones de "
        "interfaz, en particular la de agrupar el menú por trabajo y no por tabla y la de "
        "dejar un solo camino hacia cada destino, pues la versión anterior repetía cuatro "
        "enlaces en dos sitios."
    )
    d.parrafo(
        "Durante la construcción se aplicó observación directa sobre el formulario de "
        "emisión, que es la pantalla que más se usa y la única que un cajero utiliza a "
        "diario. De ahí salió su división en tres pasos, a quién se factura, qué se "
        "factura y cómo se paga, con el resumen de los totales siempre visible. La "
        "medición formal de la satisfacción, con un instrumento aplicado después del uso, "
        f"queda planificada y se declara como tal ({cita('istqb')})."
    )
