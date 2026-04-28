from database import get_all_from_table, execute_query, execute_update, get_one, get_many


def get_all_invoice_taxes():
    return get_many("SELECT * FROM impuestos ORDER BY descripcion")


def get_tax_by_id(tax_id: int):
    return get_one("SELECT * FROM impuestos WHERE cod_impuesto = %s", (tax_id,))


def create_tax(descripcion: str, porcentaje: float, codigo_dian: str = ""):
    query = "INSERT INTO impuestos (descripcion, porcentaje, codigo_dian) VALUES (%s, %s, %s)"
    return execute_query(query, (descripcion, porcentaje, codigo_dian or None))


def update_tax(tax_id: int, descripcion: str, porcentaje: float, codigo_dian: str = ""):
    query = "UPDATE impuestos SET descripcion=%s, porcentaje=%s, codigo_dian=%s WHERE cod_impuesto=%s"
    return execute_update(query, (descripcion, porcentaje, codigo_dian or None, tax_id))


def delete_tax(tax_id: int):
    return execute_update("DELETE FROM impuestos WHERE cod_impuesto = %s", (tax_id,))
