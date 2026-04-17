from database import execute_query, execute_update, get_one, get_many


def get_all_customers():
    return get_many("""
        SELECT c.*, m.nombre AS municipio_nombre, d.nombre AS departamento_nombre
        FROM customers c
        LEFT JOIN municipios m ON c.cod_municipio = m.cod_municipio
        LEFT JOIN departamentos d ON m.cod_departamento = d.cod_departamento
        WHERE c.activo = 1
        ORDER BY c.full_name
    """)


def get_customer_by_id(customer_id: int):
    return get_one("""
        SELECT c.*, m.nombre AS municipio_nombre, m.cod_departamento,
               d.nombre AS departamento_nombre
        FROM customers c
        LEFT JOIN municipios m ON c.cod_municipio = m.cod_municipio
        LEFT JOIN departamentos d ON m.cod_departamento = d.cod_departamento
        WHERE c.customer_id = %s
    """, (customer_id,))


def create_customer(full_name: str, document_type: str, document_number: str,
                    phone: str, email: str, address: str,
                    cod_municipio: str = None, pais: str = "Colombia",
                    tipo_persona: str = "NATURAL",
                    regimen_tributario: str = "NO_RESPONSABLE_IVA"):
    ciudad = ""
    departamento = ""
    if cod_municipio:
        row = get_one(
            "SELECT m.nombre, d.nombre AS dpto FROM municipios m "
            "JOIN departamentos d ON m.cod_departamento=d.cod_departamento "
            "WHERE m.cod_municipio=%s",
            (cod_municipio,)
        )
        if row:
            ciudad = row["nombre"]
            departamento = row["dpto"]
    query = """
        INSERT INTO customers
            (full_name, document_type, document_number, phone, email, address,
             ciudad, departamento, pais, tipo_persona, regimen_tributario, cod_municipio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        full_name, document_type, document_number, phone, email, address,
        ciudad, departamento, pais, tipo_persona, regimen_tributario,
        cod_municipio or None
    ))


def update_customer(customer_id: int, full_name: str, document_type: str,
                    document_number: str, phone: str, email: str, address: str,
                    cod_municipio: str = None, pais: str = "Colombia",
                    tipo_persona: str = "NATURAL",
                    regimen_tributario: str = "NO_RESPONSABLE_IVA"):
    ciudad = ""
    departamento = ""
    if cod_municipio:
        row = get_one(
            "SELECT m.nombre, d.nombre AS dpto FROM municipios m "
            "JOIN departamentos d ON m.cod_departamento=d.cod_departamento "
            "WHERE m.cod_municipio=%s",
            (cod_municipio,)
        )
        if row:
            ciudad = row["nombre"]
            departamento = row["dpto"]
    query = """
        UPDATE customers
        SET full_name=%s, document_type=%s, document_number=%s,
            phone=%s, email=%s, address=%s, ciudad=%s, departamento=%s, pais=%s,
            tipo_persona=%s, regimen_tributario=%s, cod_municipio=%s
        WHERE customer_id=%s
    """
    return execute_update(query, (
        full_name, document_type, document_number, phone, email, address,
        ciudad, departamento, pais, tipo_persona, regimen_tributario,
        cod_municipio or None, customer_id
    ))


def delete_customer(customer_id: int):
    return execute_update("UPDATE customers SET activo = 0 WHERE customer_id = %s", (customer_id,))
