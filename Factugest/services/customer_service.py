from database import get_all_from_table, execute_query, execute_update, get_one, get_many


def get_all_customers():
    return get_many("""
        SELECT * FROM customers ORDER BY full_name
    """)


def get_customer_by_id(customer_id: int):
    return get_one("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))


def create_customer(full_name: str, document_type: str, document_number: str,
                    phone: str, email: str, address: str,
                    ciudad: str = "", departamento: str = "", pais: str = "Colombia",
                    tipo_persona: str = "NATURAL", regimen_tributario: str = "NO_RESPONSABLE_IVA"):
    query = """
        INSERT INTO customers
            (full_name, document_type, document_number, phone, email, address,
             ciudad, departamento, pais, tipo_persona, regimen_tributario)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        full_name, document_type, document_number, phone, email, address,
        ciudad, departamento, pais, tipo_persona, regimen_tributario
    ))


def update_customer(customer_id: int, full_name: str, document_type: str, document_number: str,
                    phone: str, email: str, address: str,
                    ciudad: str = "", departamento: str = "", pais: str = "Colombia",
                    tipo_persona: str = "NATURAL", regimen_tributario: str = "NO_RESPONSABLE_IVA"):
    query = """
        UPDATE customers
        SET full_name=%s, document_type=%s, document_number=%s,
            phone=%s, email=%s, address=%s, ciudad=%s, departamento=%s, pais=%s,
            tipo_persona=%s, regimen_tributario=%s
        WHERE customer_id=%s
    """
    return execute_update(query, (
        full_name, document_type, document_number, phone, email, address,
        ciudad, departamento, pais, tipo_persona, regimen_tributario, customer_id
    ))


def delete_customer(customer_id: int):
    return execute_update("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
