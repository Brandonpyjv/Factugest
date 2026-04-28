from database import get_all_from_table, execute_query, execute_update, get_one


def get_all_invoice_payments():
    return get_all_from_table('pagos_factura')


def get_invoice_payment_by_id(payment_id: int):
    return get_one("SELECT * FROM pagos_factura WHERE cod_pago_factura = %s", (payment_id,))


def create_invoice_payment(status: str):
    query = "INSERT INTO pagos_factura (status) VALUES (%s)"
    return execute_query(query, (status,))


def update_invoice_payment(payment_id: int, status: str):
    query = "UPDATE pagos_factura SET status=%s WHERE cod_pago_factura=%s"
    return execute_update(query, (status, payment_id))


def delete_invoice_payment(payment_id: int):
    return execute_update("DELETE FROM pagos_factura WHERE cod_pago_factura = %s", (payment_id,))
