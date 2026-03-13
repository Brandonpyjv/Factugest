from database import create_connection

def get_all_products_detailed():
    db = create_connection()
    cursor = db.cursor(dictionary=True)

    # Seleccionamos todas las columnas de productos (p)
    # y hacemos JOIN con impuestos (i) para traer la descripción y el porcentaje
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
                   i.descripcion AS tax_name, 
                   i.porcentaje  AS cod_impuesto
            FROM productos p
                     LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto
            """

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


data=get_all_products_detailed()
print(data)
