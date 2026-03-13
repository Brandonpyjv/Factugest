from database import create_connection

def get_all_invoices_detailed():
    db = create_connection()
    cursor = db.cursor(dictionary=True)

# Eliminamos las barras invertidas; las triples comillas ya manejan el salto de línea
    query = """
            SELECT f.cod_factura, 
                   f.fecha, 
                   f.total, 
                   f.cod_metodo_pago, 
                   f.cod_pago, 
                   c.full_name  AS cliente, 
                   u.nombre  AS usuario, 
                   e.nombre  AS empresa, 
                   mp.descripcion AS metodo_pago
            FROM facturas f
                     LEFT JOIN customers c ON f.cod_cliente = c.customer_id
                     LEFT JOIN usuarios u ON f.cod_usuario = u.cod_usuario
                     LEFT JOIN empresas e ON f.cod_empresa = e.cod_empresa
                     LEFT JOIN metodos_pago mp ON f.cod_metodo_pago = mp.cod_pago
                     LEFT JOIN pagos_factura pf ON f.cod_pago = pf.cod_pago_factura
            """

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result