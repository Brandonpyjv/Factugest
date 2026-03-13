from database import get_all_from_table, execute_query, execute_update, get_one


def get_all_payment_methods():
    return get_all_from_table('metodos_pago')


def get_payment_method_by_id(pm_id: int):
    return get_one("SELECT * FROM metodos_pago WHERE cod_pago = %s", (pm_id,))


def create_payment_method(descripcion: str, nombre: str):
    query = "INSERT INTO metodos_pago (descripcion, nombre) VALUES (%s, %s)"
    return execute_query(query, (descripcion, nombre))


def update_payment_method(pm_id: int, descripcion: str, nombre: str):
    query = "UPDATE metodos_pago SET descripcion=%s, nombre=%s WHERE cod_pago=%s"
    return execute_update(query, (descripcion, nombre, pm_id))


def delete_payment_method(pm_id: int):
    return execute_update("DELETE FROM metodos_pago WHERE cod_pago = %s", (pm_id,))
