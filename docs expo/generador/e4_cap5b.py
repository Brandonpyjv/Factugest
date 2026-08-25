"""
E4 — Capítulo 5, parte B. Diseño de la base de datos, modelo entidad-relación,
modelo físico y diccionario de datos.

El diccionario se **lee del esquema real** con `esquema.py`, de manera que los
tipos, los nulos y las claves no puedan discrepar de la base. Las descripciones
salen del comentario que la propia columna trae en el esquema; donde no lo hay se
toman de `DESCRIPCIONES`, y el generador avisa si alguna columna quedó sin
describir.
"""
from pathlib import Path

import esquema

DIAGRAMAS = Path(__file__).resolve().parent.parent / "entregables" / "diagramas"
MODELO_FISICO = (Path(__file__).resolve().parent.parent /
                 "documento para que te guies claude" / "base de datos.png")

# Tablas que llevan diccionario detallado en el documento de grado.
DETALLADAS = ["clientes_api", "documentos", "facturas"]

ZONAS = [
    ("Middleware", "Lo que se emite por cuenta de terceros",
     ["clientes_api", "receptores", "documentos", "documento_lineas", "documento_eventos"]),
    ("Comercial", "Lo que el proveedor vende",
     ["facturas", "detalle_factura", "customers", "productos", "pagos_factura",
      "factura_impuesto", "factura_descuento", "producto_descuento"]),
    ("Puente", "Qué mes de qué cliente ya se cobró", ["facturas_plan"]),
    ("Compartida", "Emisores, usuarios y catálogos",
     ["empresas", "usuarios", "impuestos", "descuentos", "metodos_pago", "municipios",
      "departamentos", "auditoria", "movimientos_inventario", "logs",
      "schema_migrations"]),
]

DESCRIPCIONES = {
"clientes_api": {
    "cod_cliente_api": "Identificador interno del cliente integrado.",
    "nombre": "Nombre del negocio o del sistema integrado.",
    "cod_cliente": "Cliente comercial al que se le factura la suscripción.",
    "cod_empresa": "Empresa emisora con cuyo NIT y resolución emite este cliente.",
    "api_key_prefijo": "Parte visible de la llave, que permite localizar la fila sin "
                       "revelar el secreto.",
    "api_key_hash": "Hash de la llave completa, ya que la llave se muestra una sola vez.",
    "limite_mensual": "Documentos incluidos por mes. Sin valor cuando el plan no tiene cupo.",
    "estado": "Situación del cliente, entre activo, suspendido y revocado.",
    "plan": "Plan contratado, que determina el cupo mensual y la tarifa.",
    "creado_en": "Fecha y hora del alta del cliente.",
    "ultimo_uso": "Última vez que la llave se utilizó, para detectar integraciones inactivas.",
},
"documentos": {
    "cod_documento": "Identificador interno del documento.",
    "id_publico": "Identificador que ve el cliente integrado, que evita exponer la clave "
                  "interna.",
    "cod_empresa": "Empresa emisora con cuya resolución se numeró el documento.",
    "tipo": "Clase de documento, entre factura de venta, nota crédito y nota débito.",
    "subtotal": "Base gravable neta sobre la que se calculan los impuestos.",
    "estado": "Resultado ante la administración tributaria, entre pendiente, aceptado, "
              "rechazado y con error.",
    "referencia_externa": "Identificador de la venta en el sistema del cliente, que hace "
                          "idempotente el reintento de una emisión.",
    "cod_documento_referencia": "Factura de origen cuando el documento es una nota crédito "
                                "o débito.",
    "proveedor_dian": "Proveedor a través del cual se transmitió el documento.",
    "cod_cliente_api": "Cliente integrado por cuenta del cual se emitió.",
    "cod_receptor": "Comprador al que va dirigido el documento.",
    "prefijo": "Prefijo autorizado en la resolución del emisor.",
    "consecutivo": "Número reservado dentro del rango autorizado.",
    "numero": "Número completo del documento, con su prefijo.",
    "cufe": "Código único de facturación electrónica.",
    "fecha_emision": "Momento en que el documento fue expedido.",
    "fecha_vencimiento": "Fecha límite de pago cuando la venta es a crédito.",
    "forma_pago": "Contado o crédito.",
    "subtotal_bruto": "Suma de las líneas antes de descuentos.",
    "total_descuentos": "Descuentos de línea y de documento aplicados.",
    "total_impuestos": "Suma de los impuestos calculados sobre la base gravable.",
    "total": "Valor final del documento.",
    "motivo_nota": "Concepto de la corrección, en notas crédito y débito.",
    "observaciones": "Texto libre que el emisor incluye en el documento.",
    "orden_compra": "Referencia de la orden de compra del comprador, si la hay.",
    "xml": "Archivo XML del documento bajo el estándar UBL 2.1.",
    "creado_en": "Momento en que el registro se guardó en la base.",
},
"facturas": {
    "cod_factura": "Identificador interno de la factura.",
    "fecha": "Fecha de emisión de la factura.",
    "cod_cliente": "Cliente comercial al que se le factura el servicio.",
    "cod_usuario": "Usuario del panel que emitió la factura.",
    "cod_pago": "Estado de pago en que se encuentra la factura.",
    "total": "Valor final de la factura.",
    "cod_empresa": "Empresa emisora con cuya resolución se numeró.",
    "cod_metodo_pago": "Medio por el cual se recibió o se recibirá el pago.",
    "fecha_vencimiento": "Fecha límite de pago.",
    "subtotal": "Base gravable después de descuentos.",
    "total_descuentos": "Descuentos aplicados sobre la factura.",
    "total_impuestos": "Suma de los impuestos calculados.",
    "tipo_factura": "Tipo de documento, entre factura de venta, nota crédito y nota débito.",
    "observaciones": "Texto libre incluido en la representación gráfica.",
    "cufe": "Código único devuelto al emitir el documento por la propia API.",
    "numero_factura": "Número con que quedó expedida.",
    "forma_pago": "Contado o crédito.",
    "orden_compra": "Referencia de la orden de compra del cliente, si la hay.",
    "nombre_vendedor": "Persona que atendió la venta.",
    "cod_descuento_factura": "Descuento aplicado al total de la factura.",
    "descripcion_descuento_factura": "Concepto del descuento, que viaja hasta el PDF.",
    "cod_factura_referencia": "Factura de origen cuando el documento es una nota.",
    "motivo_nota": "Concepto de la corrección, en notas crédito y débito.",
},
}


def _filas(tabla):
    faltantes = []
    filas = []
    for nombre, tipo, nulo, clave, comentario in esquema.columnas(tabla):
        # La descripción escrita manda sobre el comentario del esquema, que está
        # redactado para quien lee el SQL y viene sin tildes.
        texto = DESCRIPCIONES.get(tabla, {}).get(nombre) or comentario
        if not texto:
            faltantes.append(f"{tabla}.{nombre}")
        filas.append([nombre, tipo, nulo, clave, texto])
    return filas, faltantes


def escribir(d):
    _diseno(d)
    _entidad_relacion(d)
    _fisico(d)
    _diccionario(d)


def _diseno(d):
    d.titulo("5.6 Diseño de la base de datos", nivel=2, nueva_pagina=True)
    d.parrafo(
        "La base de datos se diseñó sobre el modelo relacional, con integridad garantizada "
        "por claves primarias, claves foráneas y restricciones de unicidad. El acceso se "
        "realiza mediante consultas SQL explícitas y sin mapeador objeto-relacional, decisión "
        "que responde a la naturaleza del sistema, porque en la emisión de un documento "
        "importa exactamente qué sentencia se ejecuta y en qué orden."
    )
    d.parrafo(
        "La característica que distingue este diseño es que la base está organizada en dos "
        "zonas que no se mezclan, más una tabla puente que las relaciona. La zona comercial "
        "guarda lo que el proveedor vende, es decir, sus planes, sus clientes y sus facturas. "
        "La zona de middleware guarda lo que el proveedor emite por cuenta de terceros, con "
        "las empresas integradas, los compradores y los documentos electrónicos."
    )
    d.parrafo(
        "La separación no obedece a una preferencia de organización sino a una necesidad. El "
        "tablero de control y los siete reportes leen la zona comercial, de modo que un "
        "documento emitido para una empresa cliente, si se guardara allí, quedaría "
        "contabilizado como ingreso propio del proveedor. Esa confusión no produciría un error "
        "visible, sino cifras equivocadas que nadie notaría hasta comparar contra la "
        "contabilidad."
    )
    d.parrafo(
        "De esa organización se sigue que existan dos tablas para lo que parece ser lo mismo. "
        "Hay dos tablas de documentos, dos de líneas y dos de terceros, y no se trata de "
        "duplicación, porque un documento emitido por cuenta de un cliente y una factura que "
        "el proveedor cobra son hechos económicos distintos que se consultan por separado y "
        "nunca se suman."
    )
    d.tabla(
        "Organización de las tablas por zona",
        ["Zona", "Qué guarda", "Tablas"],
        [[nombre, proposito, ", ".join(tablas)] for nombre, proposito, tablas in ZONAS],
        nota="Elaboración propia. Una fila de «empresas» es un emisor, sea del proveedor o de "
             "un cliente, razón por la cual esa tabla pertenece a la zona compartida.",
        anchos=[2.3, 4.6, 9.4],
    )
    d.parrafo(
        "El consumo mensual de cada cliente se calcula contando los documentos realmente "
        "emitidos y no existe tabla de contadores. La decisión es deliberada, porque un "
        "contador almacenado puede desviarse de la realidad ante un fallo a mitad de una "
        "operación, y el día que eso ocurra el sistema cobraría una cifra distinta de la que "
        "prestó."
    )


def _entidad_relacion(d):
    d.titulo("5.7 Modelo entidad-relación conceptual", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El modelo conceptual presenta las entidades del dominio y las relaciones entre "
        "ellas, sin descender al detalle de los atributos ni a la forma en que se almacenan. "
        "Las entidades aparecen coloreadas según la zona a la que pertenecen, de manera que "
        "la separación descrita en el punto anterior resulte visible en el propio modelo."
    )
    d.figura(
        "Modelo entidad-relación conceptual",
        DIAGRAMAS / "FIG-mer.png",
        nota="Elaboración propia. Las cardinalidades se indican sobre cada relación.",
    )
    d.parrafo(
        "Tres relaciones merecen comentario. La primera es que la empresa emisora numera los "
        "documentos, mientras que el cliente API los emite. Son dos entidades distintas "
        "porque el cliente integrado es quien contrata el servicio y la empresa emisora es "
        "aquella cuya resolución de facturación se utiliza, y aunque suelen coincidir, el "
        "modelo no puede suponer que siempre lo hagan."
    )
    d.parrafo(
        "La segunda es que el receptor está relacionado con el documento y no con el cliente "
        "API. Un mismo comprador puede recibir documentos de varias empresas integradas, y "
        "atarlo a una sola obligaría a duplicarlo."
    )
    d.parrafo(
        "La tercera es la relación entre el cliente API y la factura, que es la única que "
        "cruza de una zona a la otra. Representa la tabla puente y responde a una sola "
        "pregunta, la de qué mes de qué cliente ya fue cobrado. Es el punto donde la "
        "operación del servicio y la venta del proveedor se encuentran, y conviene que sea el "
        "único."
    )


def _fisico(d):
    d.titulo("5.8 Modelo físico de la base de datos", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El modelo físico corresponde a la implementación del modelo conceptual sobre el "
        "gestor de base de datos, con los tipos de dato concretos, las claves y las "
        "relaciones declaradas. Comprende veintisiete tablas, todas con motor "
        "transaccional, condición necesaria para que la emisión de un documento pueda "
        "revertirse por completo si falla a mitad de camino."
    )
    ancho = d.seccion_horizontal()
    d.figura(
        "Modelo físico de la base de datos",
        MODELO_FISICO,
        nota="Elaboración propia. Las agrupaciones corresponden a las zonas descritas en el "
             "punto 5.6. El detalle de las tablas principales consta en el diccionario de "
             "datos del punto siguiente.",
        ancho=ancho,
    )
    d.seccion_vertical()
    d.parrafo(
        "Se presenta en orientación horizontal porque a lo ancho de una página vertical los "
        "nombres de las columnas dejan de leerse, y un diagrama que no se lee no documenta "
        "nada. Las agrupaciones del diagrama coinciden con las zonas descritas antes, y los "
        "catálogos aparecen aparte porque no participan de la operación, sino que la "
        "alimentan."
    )


def _diccionario(d):
    d.titulo("5.9 Diccionario de datos", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El diccionario de datos describe cada campo de las tablas del sistema, indicando su "
        "tipo, si admite valores nulos, si participa de alguna clave y qué información "
        "contiene. Se presentan las tres tablas que sostienen la operación, y el resto se "
        "documenta en el propio esquema de la base, donde cada columna lleva su comentario."
    )

    faltantes_totales = []
    for indice, tabla in enumerate(DETALLADAS, start=1):
        filas, faltantes = _filas(tabla)
        faltantes_totales += faltantes
        d.titulo(f"5.9.{indice} Tabla {tabla}", nivel=3, nueva_pagina=(indice > 1))
        d.parrafo(INTRO_TABLA[tabla])
        d.tabla(
            f"Diccionario de datos de la tabla {tabla}",
            ["Campo", "Tipo", "Nulo", "Clave", "Descripción"],
            filas,
            nota="Elaboración propia a partir del esquema de la base de datos. En la columna "
                 "«Clave», PK indica clave primaria y FK clave foránea.",
            anchos=[4.0, 2.6, 1.2, 1.7, 6.8],
        )
    if faltantes_totales:
        raise SystemExit(f"Columnas sin descripción: {faltantes_totales}")


INTRO_TABLA = {
"clientes_api":
    "Registra las empresas integradas con la plataforma. De esta tabla salen el plan "
    "contratado, el cupo mensual y la llave con la que el sistema del cliente se autentica. "
    "Del secreto de esa llave solo se conserva su hash, y el prefijo se guarda en claro "
    "únicamente para poder localizar la fila sin tener que comparar el hash contra todas.",
"documentos":
    "Guarda la cabecera de cada documento emitido por cuenta de terceros. Es la tabla de la "
    "que se cuenta el consumo mensual de cada cliente y sobre la que existe un índice único "
    "por empresa, tipo y número, que actúa como última defensa contra un consecutivo "
    "repetido.",
"facturas":
    "Guarda las ventas del propio proveedor, que son las mensualidades de los planes y los "
    "servicios de enganche. El número y el código único que aparecen aquí no se generan en "
    "esta tabla, sino que son los que devolvió la API al emitir el documento, porque "
    "numerarlo dos veces gastaría dos consecutivos de una resolución autorizada para una "
    "sola venta.",
}
