"""
Migraciones de esquema para Factugest.

    python migrate.py

Cada migración es idempotente: puede ejecutarse las veces que sea sin romper nada.
Lo aplicado queda registrado en la tabla `schema_migrations` para dejar traza.

El proyecto no usa ORM ni una herramienta de migraciones; este script existe para que
los cambios de esquema queden versionados en el repositorio y todo el equipo pueda
aplicarlos con un solo comando en lugar de pasarse ALTERs por chat.
"""
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


MIGRACIONES = [
    ("001", "Módulo de inventario: kardex de movimientos y flag controla_stock",
     migracion_001_inventario),
]


def run():
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
