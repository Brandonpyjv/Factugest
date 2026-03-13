import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="factugest")


def get_all_from_table(table_name):
    allowed_tables = ["customers","usuarios", "facturas","metodos_pago","descuentos", "impuestos", "empresas", "pagos_factura", "productos", "logs"]
    if table_name not in allowed_tables:
        raise ValueError("Nombre de tabla no permitido")
    db = create_connection()
    cursor = db.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    myresult = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    insert_object = [dict(zip(column_names, record)) for record in myresult]
    cursor.close()
    db.close()
    return insert_object