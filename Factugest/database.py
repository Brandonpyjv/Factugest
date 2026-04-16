import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

_DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "passwd":   os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "factugest"),
}


def create_connection():
    return mysql.connector.connect(**_DB_CONFIG)


def get_all_from_table(table_name):
    allowed_tables = [
        "customers", "usuarios", "facturas", "metodos_pago",
        "descuentos", "impuestos", "empresas", "pagos_factura",
        "productos", "logs",
    ]
    if table_name not in allowed_tables:
        raise ValueError("Nombre de tabla no permitido")
    db = create_connection()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    myresult = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    result = [dict(zip(column_names, record)) for record in myresult]
    cursor.close()
    db.close()
    return result


def execute_query(query, params=None):
    """Ejecuta INSERT y retorna el ID del nuevo registro."""
    db = create_connection()
    cursor = db.cursor()
    cursor.execute(query, params or ())
    db.commit()
    new_id = cursor.lastrowid
    cursor.close()
    db.close()
    return new_id


def execute_update(query, params=None):
    """Ejecuta UPDATE o DELETE."""
    db = create_connection()
    cursor = db.cursor()
    cursor.execute(query, params or ())
    db.commit()
    affected = cursor.rowcount
    cursor.close()
    db.close()
    return affected


def get_one(query, params=None):
    """Ejecuta un SELECT y retorna un solo registro como dict."""
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


def get_many(query, params=None):
    """Ejecuta un SELECT y retorna todos los registros como lista de dicts."""
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result
