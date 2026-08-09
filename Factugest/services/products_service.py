from database import create_connection, execute_query, execute_update, get_one


def get_all_products_detailed():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    query = """
            SELECT p.cod_producto,
                   p.sku,
                   p.nombre,
                   p.descripcion,
                   p.precio_unitario,
                   p.stock,
                   p.stock_minimo,
                   p.cod_impuesto,
                   p.unidad_medida,
                   p.codigo_barras,
                   p.activo,
                   p.tipo_item,
                   i.descripcion AS tax_name,
                   i.porcentaje  AS tax_porcentaje
            FROM productos p
                     LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto
            ORDER BY p.nombre
            """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def get_product_by_id(product_id: int):
    return get_one("SELECT * FROM productos WHERE cod_producto = %s", (product_id,))


def create_product(sku: str, nombre: str, descripcion: str, precio_unitario: float,
                   stock: int, stock_minimo: int, cod_impuesto: int,
                   unidad_medida: str, codigo_barras: str, activo: int,
                   controla_stock: int = 1):
    query = """INSERT INTO productos (sku, nombre, descripcion, precio_unitario, stock, stock_minimo,
               cod_impuesto, unidad_medida, codigo_barras, activo, controla_stock)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    return execute_query(query, (sku, nombre, descripcion, precio_unitario, stock, stock_minimo,
                                  cod_impuesto, unidad_medida, codigo_barras or None, activo,
                                  controla_stock))


def update_product(product_id: int, sku: str, nombre: str, descripcion: str,
                   precio_unitario: float, stock: int, stock_minimo: int,
                   cod_impuesto: int, unidad_medida: str, codigo_barras: str, activo: int,
                   controla_stock: int = 1):
    query = """UPDATE productos SET sku=%s, nombre=%s, descripcion=%s, precio_unitario=%s,
               stock=%s, stock_minimo=%s, cod_impuesto=%s, unidad_medida=%s,
               codigo_barras=%s, activo=%s, controla_stock=%s WHERE cod_producto=%s"""
    return execute_update(query, (sku, nombre, descripcion, precio_unitario, stock, stock_minimo,
                                   cod_impuesto, unidad_medida, codigo_barras or None, activo,
                                   controla_stock, product_id))


def delete_product(product_id: int):
    return execute_update("DELETE FROM productos WHERE cod_producto = %s", (product_id,))
