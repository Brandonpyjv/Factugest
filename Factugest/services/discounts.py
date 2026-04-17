from database import get_all_from_table, execute_query, execute_update, get_one


def get_all_discount():
    return get_all_from_table('descuentos')


def get_discount_by_id(discount_id: int):
    return get_one("SELECT * FROM descuentos WHERE cod_descuento = %s", (discount_id,))


def create_discount(descripcion: str, porcentaje: float, aplica_a_producto: int, aplica_a_factura: int):
    query = "INSERT INTO descuentos (descripcion, porcentaje, aplica_a_producto, aplica_a_factura) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (descripcion, porcentaje, aplica_a_producto, aplica_a_factura))


def update_discount(discount_id: int, descripcion: str, porcentaje: float, aplica_a_producto: int, aplica_a_factura: int):
    query = "UPDATE descuentos SET descripcion=%s, porcentaje=%s, aplica_a_producto=%s, aplica_a_factura=%s WHERE cod_descuento=%s"
    return execute_update(query, (descripcion, porcentaje, aplica_a_producto, aplica_a_factura, discount_id))


def delete_discount(discount_id: int):
    return execute_update("DELETE FROM descuentos WHERE cod_descuento = %s", (discount_id,))
