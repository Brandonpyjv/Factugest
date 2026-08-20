"""
Migraciones de esquema para Factugest.

    python migrate.py

Cada migración es idempotente: puede ejecutarse las veces que sea sin romper nada.
Lo aplicado queda registrado en la tabla `schema_migrations` para dejar traza.

El proyecto no usa ORM ni una herramienta de migraciones; este script existe para que
los cambios de esquema queden versionados en el repositorio y todo el equipo pueda
aplicarlos con un solo comando en lugar de pasarse ALTERs por chat.
"""
import sys
from datetime import datetime

from database import create_connection


# ── Helpers de introspección ────────────────────────────────────────────────

def _table_exists(cursor, table: str) -> bool:
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
        (table,),
    )
    return cursor.fetchone()[0] > 0


def _column_exists(cursor, table: str, column: str) -> bool:
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s",
        (table, column),
    )
    return cursor.fetchone()[0] > 0


def _ensure_migrations_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version     VARCHAR(50)  NOT NULL,
            descripcion VARCHAR(255) NOT NULL,
            aplicada_en DATETIME     NOT NULL,
            PRIMARY KEY (version)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)


def _already_applied(cursor, version: str) -> bool:
    cursor.execute("SELECT COUNT(*) FROM schema_migrations WHERE version = %s", (version,))
    return cursor.fetchone()[0] > 0


def _mark_applied(cursor, version: str, descripcion: str):
    cursor.execute(
        "INSERT INTO schema_migrations (version, descripcion, aplicada_en) VALUES (%s, %s, %s)",
        (version, descripcion, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )


# ── 001 · Módulo de inventario ──────────────────────────────────────────────

def migracion_001_inventario(cursor):
    """Kardex de movimientos y control de qué productos manejan stock."""
    pasos = []

    if not _table_exists(cursor, "movimientos_inventario"):
        cursor.execute("""
            CREATE TABLE movimientos_inventario (
                cod_movimiento  INT(11)       NOT NULL AUTO_INCREMENT,
                cod_producto    INT(11)       NOT NULL,
                tipo            VARCHAR(10)   NOT NULL COMMENT 'ENTRADA | SALIDA | AJUSTE',
                motivo          VARCHAR(30)   NOT NULL COMMENT 'VENTA, COMPRA, DEVOLUCION, AJUSTE_MANUAL, MERMA, INICIAL, ANULACION',
                cantidad        INT(11)       NOT NULL COMMENT 'Siempre positivo; el signo lo determina el tipo',
                stock_anterior  INT(11)       NOT NULL,
                stock_nuevo     INT(11)       NOT NULL,
                costo_unitario  DECIMAL(12,2)          DEFAULT NULL,
                cod_factura     INT(11)                DEFAULT NULL,
                cod_usuario     INT(11)                DEFAULT NULL,
                observaciones   VARCHAR(255)           DEFAULT NULL,
                fecha           DATETIME(6)   NOT NULL,
                PRIMARY KEY (cod_movimiento),
                KEY idx_mov_producto (cod_producto),
                KEY idx_mov_fecha    (fecha),
                KEY idx_mov_factura  (cod_factura),
                CONSTRAINT fk_mov_producto FOREIGN KEY (cod_producto)
                    REFERENCES productos (cod_producto) ON DELETE CASCADE,
                CONSTRAINT fk_mov_usuario  FOREIGN KEY (cod_usuario)
                    REFERENCES usuarios (cod_usuario)  ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla movimientos_inventario creada")

    if not _column_exists(cursor, "productos", "controla_stock"):
        cursor.execute(
            "ALTER TABLE productos ADD COLUMN controla_stock TINYINT(1) NOT NULL DEFAULT 1 "
            "COMMENT '0 = servicio o intangible: no descuenta inventario' AFTER stock_minimo"
        )
        # WSD es la unidad DIAN de servicio: no tiene sentido llevarle inventario.
        cursor.execute("UPDATE productos SET controla_stock = 0 WHERE unidad_medida = 'WSD'")
        pasos.append("columna productos.controla_stock creada")

    # Saldo de apertura: sin esto el kardex arranca vacío y no cuadraría con el stock actual.
    cursor.execute("SELECT COUNT(*) FROM movimientos_inventario WHERE motivo = 'INICIAL'")
    if cursor.fetchone()[0] == 0:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO movimientos_inventario
                (cod_producto, tipo, motivo, cantidad, stock_anterior, stock_nuevo,
                 costo_unitario, observaciones, fecha)
            SELECT cod_producto, 'ENTRADA', 'INICIAL', COALESCE(stock, 0), 0, COALESCE(stock, 0),
                   precio_unitario, 'Saldo de apertura al implementar el kardex', %s
            FROM productos
            WHERE controla_stock = 1
        """, (ahora,))
        pasos.append(f"{cursor.rowcount} saldos de apertura registrados")

    return pasos


# ── 002 · Foto de perfil ────────────────────────────────────────────────────

def migracion_002_foto_perfil(cursor):
    """Foto de perfil del usuario, mostrada en el navbar y el listado."""
    pasos = []

    if not _column_exists(cursor, "usuarios", "foto"):
        cursor.execute(
            "ALTER TABLE usuarios ADD COLUMN foto VARCHAR(255) DEFAULT NULL "
            "COMMENT 'Nombre del archivo dentro de static/img/perfiles; NULL = avatar genérico' "
            "AFTER rol"
        )
        pasos.append("columna usuarios.foto creada")

    return pasos


# ── 003 · API middleware DIAN ───────────────────────────────────────────────

def migracion_003_api_middleware(cursor):
    """Tablas de los documentos que emitimos por cuenta de terceros.

    Están separadas de `facturas` a propósito: ahí van nuestras ventas de planes,
    y meter las facturas de nuestros clientes las contaría como ingresos propios
    en el tablero y en los reportes.
    """
    pasos = []

    if not _table_exists(cursor, "clientes_api"):
        cursor.execute("""
            CREATE TABLE clientes_api (
                cod_cliente_api INT(11)      NOT NULL AUTO_INCREMENT,
                nombre          VARCHAR(150) NOT NULL COMMENT 'Nombre del negocio o sistema integrado',
                cod_cliente     INT(11)               DEFAULT NULL COMMENT 'customers: a quien le facturamos el plan',
                cod_empresa     INT(11)      NOT NULL COMMENT 'empresas: con que NIT y resolucion emite',
                api_key_prefijo VARCHAR(20)  NOT NULL COMMENT 'Parte visible de la llave; permite ubicar la fila sin revelarla',
                api_key_hash    VARCHAR(255) NOT NULL COMMENT 'Hash de la llave completa; la llave se muestra una sola vez',
                plan            VARCHAR(20)  NOT NULL DEFAULT 'BASICO',
                limite_mensual  INT(11)               DEFAULT NULL COMMENT 'Documentos por mes; NULL = sin limite',
                estado          VARCHAR(20)  NOT NULL DEFAULT 'ACTIVO' COMMENT 'ACTIVO | SUSPENDIDO | REVOCADO',
                creado_en       DATETIME     NOT NULL,
                ultimo_uso      DATETIME              DEFAULT NULL,
                PRIMARY KEY (cod_cliente_api),
                UNIQUE KEY uq_api_key_prefijo (api_key_prefijo),
                KEY idx_cliente_api_empresa (cod_empresa),
                KEY idx_cliente_api_cliente (cod_cliente),
                CONSTRAINT fk_cliente_api_empresa FOREIGN KEY (cod_empresa)
                    REFERENCES empresas (cod_empresa),
                CONSTRAINT fk_cliente_api_cliente FOREIGN KEY (cod_cliente)
                    REFERENCES customers (customer_id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla clientes_api creada")

    if not _table_exists(cursor, "receptores"):
        cursor.execute("""
            CREATE TABLE receptores (
                cod_receptor       INT(11)      NOT NULL AUTO_INCREMENT,
                cod_cliente_api    INT(11)      NOT NULL,
                tipo_documento     VARCHAR(4)   NOT NULL COMMENT 'Codigo DIAN: 13 CC, 22 CE, 31 NIT, 41 Pasaporte',
                numero_documento   VARCHAR(30)  NOT NULL,
                dv                 CHAR(1)               DEFAULT NULL,
                nombre             VARCHAR(200) NOT NULL,
                tipo_persona       VARCHAR(20)           DEFAULT 'NATURAL',
                regimen_tributario VARCHAR(60)           DEFAULT 'NO_RESPONSABLE_IVA',
                email              VARCHAR(150)          DEFAULT NULL,
                telefono           VARCHAR(40)           DEFAULT NULL,
                direccion          VARCHAR(200)          DEFAULT NULL,
                cod_municipio      CHAR(5)               DEFAULT NULL,
                creado_en          DATETIME     NOT NULL,
                PRIMARY KEY (cod_receptor),
                -- El mismo comprador enviado dos veces se reutiliza en lugar de duplicarse,
                -- y cada cliente API ve solo su propio padron.
                UNIQUE KEY uq_receptor_del_cliente (cod_cliente_api, tipo_documento, numero_documento),
                CONSTRAINT fk_receptor_cliente_api FOREIGN KEY (cod_cliente_api)
                    REFERENCES clientes_api (cod_cliente_api) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla receptores creada")

    if not _table_exists(cursor, "documentos"):
        cursor.execute("""
            CREATE TABLE documentos (
                cod_documento      INT(11)       NOT NULL AUTO_INCREMENT,
                id_publico         VARCHAR(40)   NOT NULL COMMENT 'Identificador que ve el cliente; no exponemos el autoincremental',
                cod_cliente_api    INT(11)       NOT NULL,
                cod_empresa        INT(11)       NOT NULL COMMENT 'Emisor con cuya resolucion se numero',
                cod_receptor       INT(11)       NOT NULL,
                tipo               VARCHAR(5)    NOT NULL DEFAULT 'FV' COMMENT 'FV | NC | ND',
                prefijo            VARCHAR(10)            DEFAULT NULL,
                consecutivo        BIGINT(20)             DEFAULT NULL,
                numero             VARCHAR(50)            DEFAULT NULL,
                cufe               VARCHAR(200)           DEFAULT NULL,
                fecha_emision      DATETIME(6)   NOT NULL,
                fecha_vencimiento  DATE                   DEFAULT NULL,
                forma_pago         VARCHAR(20)   NOT NULL DEFAULT 'CONTADO',
                subtotal_bruto     DECIMAL(14,2) NOT NULL DEFAULT 0,
                total_descuentos   DECIMAL(14,2) NOT NULL DEFAULT 0,
                subtotal           DECIMAL(14,2) NOT NULL DEFAULT 0 COMMENT 'Base gravable neta',
                total_impuestos    DECIMAL(14,2) NOT NULL DEFAULT 0,
                total              DECIMAL(14,2) NOT NULL DEFAULT 0,
                estado             VARCHAR(20)   NOT NULL DEFAULT 'PENDIENTE' COMMENT 'PENDIENTE | ACEPTADO | RECHAZADO | ERROR',
                referencia_externa VARCHAR(80)            DEFAULT NULL COMMENT 'Identificador de la venta en el sistema del cliente',
                cod_documento_referencia INT(11)          DEFAULT NULL COMMENT 'La FV que origina una NC o ND',
                motivo_nota        TEXT                   DEFAULT NULL,
                observaciones      TEXT                   DEFAULT NULL,
                orden_compra       VARCHAR(100)           DEFAULT NULL,
                proveedor_dian     VARCHAR(20)            DEFAULT NULL COMMENT 'simulado | factus',
                -- Se guarda el XML y no el PDF: el XML es lo que se firma y valida, y hay
                -- deber de conservarlo. La representacion grafica se regenera de estos datos.
                xml                MEDIUMTEXT             DEFAULT NULL,
                creado_en          DATETIME      NOT NULL,
                PRIMARY KEY (cod_documento),
                UNIQUE KEY uq_documento_publico (id_publico),
                -- Idempotencia: reintentar la misma venta no emite un segundo documento.
                -- MySQL admite varios NULL en un indice unico, asi que quien no manda
                -- referencia no queda bloqueado.
                UNIQUE KEY uq_referencia_del_cliente (cod_cliente_api, referencia_externa),
                -- Red de seguridad sobre la reserva atomica del consecutivo: aunque la
                -- aplicacion se equivoque, la base no acepta dos veces el mismo numero.
                UNIQUE KEY uq_numero_del_emisor (cod_empresa, tipo, numero),
                KEY idx_documento_cliente (cod_cliente_api),
                KEY idx_documento_fecha (fecha_emision),
                KEY idx_documento_estado (estado),
                KEY idx_documento_referencia (cod_documento_referencia),
                CONSTRAINT fk_documento_cliente_api FOREIGN KEY (cod_cliente_api)
                    REFERENCES clientes_api (cod_cliente_api),
                CONSTRAINT fk_documento_empresa FOREIGN KEY (cod_empresa)
                    REFERENCES empresas (cod_empresa),
                CONSTRAINT fk_documento_receptor FOREIGN KEY (cod_receptor)
                    REFERENCES receptores (cod_receptor),
                CONSTRAINT fk_documento_referencia FOREIGN KEY (cod_documento_referencia)
                    REFERENCES documentos (cod_documento) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla documentos creada")

    if not _table_exists(cursor, "documento_lineas"):
        cursor.execute("""
            CREATE TABLE documento_lineas (
                cod_linea             INT(11)       NOT NULL AUTO_INCREMENT,
                cod_documento         INT(11)       NOT NULL,
                orden                 INT(11)       NOT NULL DEFAULT 1,
                -- No es FK a productos: el catalogo es del sistema del cliente, no nuestro.
                codigo                VARCHAR(60)            DEFAULT NULL COMMENT 'SKU en el sistema del cliente',
                descripcion           VARCHAR(300)  NOT NULL,
                unidad_medida         VARCHAR(10)            DEFAULT '94',
                -- Con decimales porque la DIAN admite unidades fraccionarias (kilos, horas);
                -- nuestro detalle_factura interno solo maneja enteros.
                cantidad              DECIMAL(14,3) NOT NULL,
                precio_unitario       DECIMAL(14,2) NOT NULL,
                valor_bruto           DECIMAL(14,2) NOT NULL DEFAULT 0,
                descuento_porcentaje  DECIMAL(6,3)  NOT NULL DEFAULT 0,
                descuento_valor       DECIMAL(14,2) NOT NULL DEFAULT 0,
                descripcion_descuento VARCHAR(200)           DEFAULT NULL,
                subtotal              DECIMAL(14,2) NOT NULL DEFAULT 0 COMMENT 'Base gravable de la linea',
                impuesto_codigo_dian  VARCHAR(5)             DEFAULT '01',
                impuesto_porcentaje   DECIMAL(6,3)  NOT NULL DEFAULT 0,
                impuesto_valor        DECIMAL(14,2) NOT NULL DEFAULT 0,
                PRIMARY KEY (cod_linea),
                KEY idx_linea_documento (cod_documento),
                CONSTRAINT fk_linea_documento FOREIGN KEY (cod_documento)
                    REFERENCES documentos (cod_documento) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla documento_lineas creada")

    if not _table_exists(cursor, "documento_eventos"):
        cursor.execute("""
            CREATE TABLE documento_eventos (
                cod_evento    INT(11)     NOT NULL AUTO_INCREMENT,
                cod_documento INT(11)     NOT NULL,
                tipo          VARCHAR(30) NOT NULL COMMENT 'RECIBIDO | TRANSMITIDO | ACEPTADO | RECHAZADO | CORREO_ENVIADO | ERROR',
                proveedor     VARCHAR(20)          DEFAULT NULL,
                codigo        VARCHAR(20)          DEFAULT NULL COMMENT 'Codigo de respuesta del proveedor',
                mensaje       TEXT                 DEFAULT NULL,
                -- Respuesta cruda del proveedor: si la DIAN rechaza, hay que poder mostrar
                -- exactamente que contesto y no una interpretacion nuestra.
                payload       MEDIUMTEXT           DEFAULT NULL,
                fecha         DATETIME(6) NOT NULL,
                PRIMARY KEY (cod_evento),
                KEY idx_evento_documento (cod_documento),
                KEY idx_evento_fecha (fecha),
                CONSTRAINT fk_evento_documento FOREIGN KEY (cod_documento)
                    REFERENCES documentos (cod_documento) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla documento_eventos creada")

    # No hay tabla de consumo: los documentos por cliente y por mes se cuentan de
    # `documentos`, de modo que el contador nunca puede desviarse de la realidad.

    return pasos


# ── 004 · Tipos de documento con los códigos de la DIAN ─────────────────────

# El catálogo anterior era propio (C, E, J, G) y no correspondía al del anexo
# técnico, así que `xml_service` traducía a mano y se equivocaba: mandaba un
# cliente jurídico con esquema 13 (cédula) en lugar de 31 (NIT). Las entidades
# públicas —la «G» de gobierno— también se identifican con NIT; la DIAN no tiene
# un código aparte para ellas.
_MAPEO_TIPOS = {
    "C": "13",   # Cédula de ciudadanía
    "E": "22",   # Cédula de extranjería
    "J": "31",   # NIT
    "N": "31",   # NIT (lo que xml_service ya trataba como NIT)
    "G": "31",   # Gobierno → NIT
}


def migracion_004_tipos_documento_dian(cursor):
    """Convierte customers.document_type al código DIAN."""
    pasos = []

    cursor.execute(
        "SELECT COLUMN_TYPE FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'customers' "
        "AND COLUMN_NAME = 'document_type'"
    )
    fila = cursor.fetchone()
    tipo_actual = (fila[0] if fila else "").lower()

    # Un char(1) no alcanza para un código de dos dígitos: hay que ensanchar antes
    # de convertir, o el UPDATE truncaría los valores.
    if tipo_actual != "varchar(4)":
        cursor.execute(
            "ALTER TABLE customers MODIFY document_type VARCHAR(4) NOT NULL DEFAULT '13' "
            "COMMENT 'Código DIAN: 13 CC, 22 CE, 31 NIT, 41 Pasaporte'"
        )
        pasos.append("columna customers.document_type ensanchada a VARCHAR(4)")

    for viejo, nuevo in _MAPEO_TIPOS.items():
        cursor.execute(
            "UPDATE customers SET document_type = %s WHERE document_type = %s",
            (nuevo, viejo),
        )
        if cursor.rowcount:
            pasos.append(f"{cursor.rowcount} cliente(s) con '{viejo}' pasan a '{nuevo}'")

    # Lo que no estaba en el catálogo viejo ni es un código válido se deja como
    # cédula, que es el caso mayoritario, pero se reporta para poder revisarlo.
    codigos = ", ".join(f"'{c}'" for c in
                        ("11", "12", "13", "21", "22", "31", "41", "42", "50", "91"))
    cursor.execute(f"SELECT COUNT(*) FROM customers WHERE document_type NOT IN ({codigos})")
    sueltos = cursor.fetchone()[0]
    if sueltos:
        cursor.execute(f"UPDATE customers SET document_type = '13' "
                       f"WHERE document_type NOT IN ({codigos})")
        pasos.append(f"ATENCION: {sueltos} cliente(s) con un tipo desconocido quedaron en '13'")

    return pasos


# ── 005 · Líneas de concepto en el detalle ──────────────────────────────────

def migracion_005_lineas_de_concepto(cursor):
    """Permite que una línea describa un concepto y no un producto del catálogo.

    Una nota débito ajusta un flete, un interés o un cargo: no hay un producto
    al que apuntar. Se emitían sin ninguna línea, así que su XML salía sin
    InvoiceLine y la DIAN lo habría rechazado.
    """
    pasos = []

    cursor.execute(
        "SELECT IS_NULLABLE FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'detalle_factura' "
        "AND COLUMN_NAME = 'cod_producto'"
    )
    fila = cursor.fetchone()
    if fila and fila[0] == "NO":
        cursor.execute(
            "ALTER TABLE detalle_factura MODIFY cod_producto INT(11) DEFAULT NULL "
            "COMMENT 'NULL cuando la linea es un concepto y no un producto'"
        )
        pasos.append("detalle_factura.cod_producto ahora admite NULL")

    if not _column_exists(cursor, "detalle_factura", "descripcion"):
        cursor.execute(
            "ALTER TABLE detalle_factura ADD COLUMN descripcion VARCHAR(300) DEFAULT NULL "
            "COMMENT 'Texto de la linea cuando no hay producto; si hay, manda el del producto' "
            "AFTER cod_producto"
        )
        pasos.append("columna detalle_factura.descripcion creada")

    # Las notas débito ya emitidas no tienen líneas. Se reconstruye la suya a
    # partir de la cabecera, que es donde quedó el ajuste, para que dejen de ser
    # documentos que ningún proveedor aceptaría.
    cursor.execute("""
        SELECT f.cod_factura, f.subtotal, f.total_impuestos, f.motivo_nota
        FROM facturas f
        LEFT JOIN detalle_factura d ON f.cod_factura = d.cod_factura
        WHERE f.tipo_factura = 'ND'
        GROUP BY f.cod_factura, f.subtotal, f.total_impuestos, f.motivo_nota
        HAVING COUNT(d.cod_destalle) = 0
    """)
    huerfanas = cursor.fetchall()
    for cod_factura, subtotal, impuestos, motivo in huerfanas:
        subtotal = float(subtotal or 0)
        impuestos = float(impuestos or 0)
        tasa = round(impuestos / subtotal * 100, 2) if subtotal else 0
        cursor.execute(
            "INSERT INTO detalle_factura "
            "  (cod_factura, cod_producto, descripcion, cantidad, precio_unitario, "
            "   subtotal, descuento_porcentaje, descuento_valor, "
            "   impuesto_porcentaje, impuesto_valor) "
            "VALUES (%s, NULL, %s, 1, %s, %s, 0, 0, %s, %s)",
            (cod_factura, (motivo or "Ajuste")[:300], subtotal, subtotal, tasa, impuestos),
        )
    if huerfanas:
        pasos.append(f"{len(huerfanas)} nota(s) debito sin lineas: linea reconstruida")

    return pasos


# ── 008 · Guardar el QR del documento ───────────────────────────────────────

def migracion_008_qr_del_documento(cursor):
    """El enlace de verificación se guarda, no solo se devuelve.

    Venía en la respuesta de la emisión pero no se persistía, así que
    `GET /documentos/{id}` y el reintento idempotente lo devolvían vacío: el
    cliente que perdía la primera respuesta se quedaba sin el QR para siempre.
    """
    pasos = []
    if not _column_exists(cursor, "documentos", "qr"):
        cursor.execute(
            "ALTER TABLE documentos ADD COLUMN qr VARCHAR(255) DEFAULT NULL "
            "COMMENT 'Enlace de verificacion que va en la representacion grafica' "
            "AFTER cufe")
        pasos.append("columna documentos.qr creada")
    return pasos


# ── 009 · Facturación mensual del plan ──────────────────────────────────────

def migracion_009_facturacion_de_planes(cursor):
    """Puente entre la mensualidad que le cobramos a un cliente y lo que emitimos.

    Una fila por cliente y periodo, y no dos columnas en `facturas`: la venta del
    plan es una factura nuestra corriente —el tablero y los reportes la cuentan
    como cualquier otra— y esto es solo el registro de que ese mes ya se cobró.
    El índice único es lo que impide cobrar dos veces el mismo mes; sin él, dos
    clics en el botón dejarían al cliente con dos mensualidades idénticas.

    `cod_documento` guarda el documento electrónico con el que se emitió, que sale
    de llamar a nuestra propia API: la mensualidad de un cliente de FactuGest la
    emite FactuGest con el mismo servicio que le vende.
    """
    pasos = []

    if not _table_exists(cursor, "facturas_plan"):
        cursor.execute("""
            CREATE TABLE facturas_plan (
                cod_factura_plan     INT(11)  NOT NULL AUTO_INCREMENT,
                cod_cliente_api      INT(11)  NOT NULL,
                periodo              CHAR(7)  NOT NULL COMMENT 'Mes cobrado, AAAA-MM',
                cod_factura          INT(11)  NOT NULL COMMENT 'La venta en facturas',
                cod_documento        INT(11)           DEFAULT NULL COMMENT 'Documento electronico emitido por nuestra propia API',
                documentos_emitidos  INT(11)  NOT NULL DEFAULT 0 COMMENT 'Consumo real del periodo, congelado al facturar',
                documentos_excedente INT(11)  NOT NULL DEFAULT 0,
                creado_en            DATETIME NOT NULL,
                PRIMARY KEY (cod_factura_plan),
                UNIQUE KEY uq_plan_periodo (cod_cliente_api, periodo),
                KEY idx_plan_factura (cod_factura),
                CONSTRAINT fk_plan_cliente_api FOREIGN KEY (cod_cliente_api)
                    REFERENCES clientes_api (cod_cliente_api) ON DELETE CASCADE,
                CONSTRAINT fk_plan_factura FOREIGN KEY (cod_factura)
                    REFERENCES facturas (cod_factura) ON DELETE CASCADE,
                CONSTRAINT fk_plan_documento FOREIGN KEY (cod_documento)
                    REFERENCES documentos (cod_documento) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla facturas_plan creada")

    # El precio del plan no se guarda aquí: es el del producto de servicio con SKU
    # PLAN-<plan>, para que subir la tarifa sea editar un producto y no migrar datos.
    return pasos


# ── 010 · Auditoría ─────────────────────────────────────────────────────────

def migracion_010_auditoria(cursor):
    """Quién hizo qué, cuándo y desde dónde.

    Había una tabla `logs` con cinco columnas en la que nunca se escribió: sin
    quién, sin sobre qué, sin desde dónde. Un registro que no se llena no es un
    registro; era un lugar donde algún día se iba a escribir algo.

    Tres decisiones que conviene entender antes de tocar esto:

    **Una sola tabla y no una por módulo.** La auditoría se lee en orden
    cronológico y se filtra —qué hizo Yuliana ayer, qué le pasó a la factura
    FG60—. Repartida en ocho tablas, cada una de esas preguntas sería una unión
    de ocho consultas.

    **Se guarda el nombre del usuario, no solo su código.** Si mañana se borra o
    se renombra, el registro tiene que seguir diciendo quién fue. Una auditoría
    que cambia cuando cambian los datos que audita no sirve de prueba.

    **La descripción se escribe en el momento.** No se reconstruye después
    leyendo la factura, porque la factura pudo anularse, cambiar o desaparecer.
    Lo que quedó escrito es lo que pasó ese día.
    """
    pasos = []

    if not _table_exists(cursor, "auditoria"):
        cursor.execute("""
            CREATE TABLE auditoria (
                cod_auditoria  BIGINT       NOT NULL AUTO_INCREMENT,
                fecha          DATETIME(6)  NOT NULL,
                cod_usuario    INT(11)               DEFAULT NULL,
                usuario_nombre VARCHAR(120)          DEFAULT NULL COMMENT 'Copia del nombre: el registro sobrevive al usuario',
                usuario_rol    VARCHAR(20)           DEFAULT NULL,
                accion         VARCHAR(30)  NOT NULL COMMENT 'INGRESO | SALIDA | CREO | ACTUALIZO | ELIMINO | EMITIO | ANULO | ...',
                entidad        VARCHAR(40)           DEFAULT NULL COMMENT 'Sobre que se actuo: factura, cliente, producto...',
                entidad_id     VARCHAR(60)           DEFAULT NULL COMMENT 'Su identificador, como texto: hay codigos y numeros de factura',
                descripcion    VARCHAR(300) NOT NULL COMMENT 'Una frase legible, escrita en el momento',
                cambios        MEDIUMTEXT            DEFAULT NULL COMMENT 'JSON con el antes y el despues, solo en modificaciones',
                ip             VARCHAR(45)           DEFAULT NULL,
                PRIMARY KEY (cod_auditoria),
                KEY idx_auditoria_fecha (fecha),
                KEY idx_auditoria_usuario (cod_usuario),
                KEY idx_auditoria_entidad (entidad, entidad_id),
                KEY idx_auditoria_accion (accion),
                -- ON DELETE SET NULL y no CASCADE: borrar un usuario no puede
                -- borrar el rastro de lo que hizo. Para eso queda su nombre.
                CONSTRAINT fk_auditoria_usuario FOREIGN KEY (cod_usuario)
                    REFERENCES usuarios (cod_usuario) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        pasos.append("tabla auditoria creada")

    # La tabla vieja se va: nunca se escribió en ella y mantenerla al lado de la
    # nueva solo invita a que alguien escriba en la equivocada.
    if _table_exists(cursor, "logs"):
        cursor.execute("SELECT COUNT(*) FROM logs")
        cuantos = cursor.fetchall()[0]
        cuantos = list(cuantos.values())[0] if isinstance(cuantos, dict) else cuantos[0]
        if cuantos:
            pasos.append(f"tabla logs conservada: tiene {cuantos} fila(s) que revisar")
        else:
            cursor.execute("DROP TABLE logs")
            pasos.append("tabla logs eliminada (estaba vacía)")

    return pasos


# ── 011 · Logo por empresa emisora ──────────────────────────────────────────

def migracion_011_logo_por_empresa(cursor):
    """El membrete de cada emisor lleva su propio logo.

    El PDF tenía la ruta del logo de FactuGest escrita en el código y lo
    estampaba en todos los documentos, incluidos los que emitimos por cuenta de
    terceros: la factura de una clínica salía con nuestra marca, como si la
    hubiéramos expedido nosotros. Eso no es un detalle estético —es un documento
    fiscal diciendo quién lo emitió—.

    Sin logo cargado, el PDF pone el nombre del emisor en negrilla. La DIAN no
    exige logo; lo que no puede llevar es uno ajeno.
    """
    pasos = []
    if not _column_exists(cursor, "empresas", "logo"):
        cursor.execute(
            "ALTER TABLE empresas ADD COLUMN logo VARCHAR(255) DEFAULT NULL "
            "COMMENT 'Archivo dentro de static/img/logos; NULL = se imprime el nombre' "
            "AFTER website")
        pasos.append("columna empresas.logo creada")
    return pasos


# ── 012 · Color de marca de cada emisor ─────────────────────────────────────

def migracion_012_color_de_marca(cursor):
    """El PDF se pinta con el color del emisor, no con el nuestro.

    Los encabezados de tabla, las líneas y los totales salían en el azul de
    FactuGest en todas las facturas. Junto con el logo, hacía que el documento de
    un cliente pareciera nuestro: una comercializadora con marca roja recibía sus
    facturas en azul corporativo ajeno.

    Se guarda como hexadecimal porque es lo que entiende tanto el PDF como el
    selector de color del navegador, y porque una paleta con nombre obligaría a
    mantener una tabla de paletas para no ganar nada.
    """
    pasos = []
    if not _column_exists(cursor, "empresas", "color_marca"):
        cursor.execute(
            "ALTER TABLE empresas ADD COLUMN color_marca CHAR(7) DEFAULT NULL "
            "COMMENT 'Color del membrete y las tablas del PDF, en #rrggbb' AFTER logo")
        pasos.append("columna empresas.color_marca creada")
    return pasos


# ── 013 · Concepto del descuento de factura en los documentos de la API ─────

def migracion_013_concepto_del_descuento(cursor):
    """El nombre del descuento global que envía el integrador.

    La API lo recibe —`descuento_global.descripcion`— y se perdía al guardar: no
    había columna. El PDF terminaba diciendo «(-) Dto. de factura (5.0%)» sin
    poder explicar de qué descuento se trataba, mientras que en el formulario web
    sí salía. Lo que el contrato acepta, se guarda.
    """
    pasos = []
    if not _column_exists(cursor, "documentos", "descripcion_descuento_factura"):
        cursor.execute(
            "ALTER TABLE documentos ADD COLUMN descripcion_descuento_factura "
            "VARCHAR(200) DEFAULT NULL COMMENT 'Concepto del descuento global, tal "
            "como lo envio el integrador' AFTER total_descuentos")
        pasos.append("columna documentos.descripcion_descuento_factura creada")
    return pasos


MIGRACIONES = [
    ("001", "Módulo de inventario: kardex de movimientos y flag controla_stock",
     migracion_001_inventario),
    ("002", "Foto de perfil de usuario",
     migracion_002_foto_perfil),
    ("003", "API middleware DIAN: clientes API, receptores, documentos, líneas y eventos",
     migracion_003_api_middleware),
    ("004", "Tipos de documento de cliente con los códigos de la DIAN",
     migracion_004_tipos_documento_dian),
    ("005", "Líneas de concepto en detalle_factura y reconstrucción de las notas débito",
     migracion_005_lineas_de_concepto),
    ("008", "Guardar el QR de verificación del documento",
     migracion_008_qr_del_documento),
    ("009", "Facturación mensual del plan: puente entre la venta y el documento emitido",
     migracion_009_facturacion_de_planes),
    ("010", "Auditoría: quién hizo qué, cuándo y desde dónde",
     migracion_010_auditoria),
    ("011", "Logo propio de cada empresa emisora",
     migracion_011_logo_por_empresa),
    ("012", "Color de marca de cada empresa emisora",
     migracion_012_color_de_marca),
    ("013", "Concepto del descuento de factura en los documentos de la API",
     migracion_013_concepto_del_descuento),
]


def run():
    # La consola de Windows usa cp1252 y un acento o una flecha en el mensaje de una
    # migración bastaba para tumbarla a mitad de camino. El texto que se imprime no
    # debería poder abortar un cambio de esquema.
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

    db = create_connection()
    cursor = db.cursor()
    try:
        _ensure_migrations_table(cursor)
        db.commit()

        for version, descripcion, funcion in MIGRACIONES:
            if _already_applied(cursor, version):
                print(f"  [=] {version} ya aplicada — se omite")
                continue

            print(f"  [>] Aplicando {version}: {descripcion}")
            for paso in funcion(cursor):
                print(f"      · {paso}")
            _mark_applied(cursor, version, descripcion)
            db.commit()
            print(f"  [OK] {version} aplicada")
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    print("Factugest — migraciones de esquema")
    run()
    print("Listo.")
