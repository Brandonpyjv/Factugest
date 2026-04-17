from database import create_connection, execute_query, execute_update, get_one, get_many


def get_all_invoices_detailed():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT f.cod_factura,
               f.numero_factura,
               f.fecha,
               f.fecha_vencimiento,
               f.total,
               f.subtotal,
               f.total_descuentos,
               f.total_impuestos,
               f.tipo_factura,
               f.cod_metodo_pago,
               f.cod_pago,
               f.observaciones,
               c.full_name        AS cliente,
               c.document_number  AS cliente_doc,
               u.nombre           AS usuario,
               e.nombre           AS empresa,
               mp.descripcion     AS metodo_pago,
               pf.status          AS estado_pago
        FROM facturas f
            LEFT JOIN customers c    ON f.cod_cliente    = c.customer_id
            LEFT JOIN usuarios u     ON f.cod_usuario    = u.cod_usuario
            LEFT JOIN empresas e     ON f.cod_empresa    = e.cod_empresa
            LEFT JOIN metodos_pago mp ON f.cod_metodo_pago = mp.cod_pago
            LEFT JOIN pagos_factura pf ON f.cod_pago      = pf.cod_pago_factura
        ORDER BY f.fecha DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def get_invoice_by_numero_factura(numero_factura: str):
    return get_one("""
        SELECT f.*,
               c.full_name          AS cliente_nombre,
               c.document_type,
               c.document_number,
               c.phone              AS cliente_phone,
               c.email              AS cliente_email,
               c.address            AS cliente_address,
               c.ciudad             AS cliente_ciudad,
               c.departamento       AS cliente_departamento,
               c.cod_municipio      AS cliente_cod_municipio,
               c.tipo_persona,
               c.regimen_tributario AS cliente_regimen,
               u.nombre             AS usuario_nombre,
               e.nombre             AS empresa_nombre,
               e.nit                AS empresa_nit,
               e.dv                 AS empresa_dv,
               e.direccion          AS empresa_direccion,
               e.ciudad             AS empresa_ciudad,
               e.telefono           AS empresa_telefono,
               e.correo             AS empresa_correo,
               e.website            AS empresa_website,
               e.regimen_tributario AS empresa_regimen,
               e.actividad_economica,
               e.tarifa_ica         AS empresa_tarifa_ica,
               e.autoretenedor      AS empresa_autoretenedor,
               e.gran_contribuyente AS empresa_gran_contribuyente,
               e.prefijo_factura    AS empresa_prefijo,
               e.resolucion_dian    AS empresa_resolucion_dian,
               e.resolucion_fecha_desde AS empresa_resolucion_fecha_desde,
               e.resolucion_fecha_hasta AS empresa_resolucion_fecha_hasta,
               e.resolucion_desde   AS empresa_resolucion_desde,
               e.resolucion_hasta   AS empresa_resolucion_hasta,
               e.cod_municipio      AS empresa_cod_municipio,
               mp.descripcion       AS metodo_pago_nombre,
               pf.status            AS estado_pago
        FROM facturas f
            LEFT JOIN customers c     ON f.cod_cliente     = c.customer_id
            LEFT JOIN usuarios u      ON f.cod_usuario     = u.cod_usuario
            LEFT JOIN empresas e      ON f.cod_empresa     = e.cod_empresa
            LEFT JOIN metodos_pago mp ON f.cod_metodo_pago = mp.cod_pago
            LEFT JOIN pagos_factura pf ON f.cod_pago       = pf.cod_pago_factura
        WHERE f.numero_factura = %s
    """, (numero_factura,))


def get_invoice_by_id(invoice_id: int):
    return get_one("""
        SELECT f.*,
               c.full_name          AS cliente_nombre,
               c.document_type,
               c.document_number,
               c.phone              AS cliente_phone,
               c.email              AS cliente_email,
               c.address            AS cliente_address,
               c.ciudad             AS cliente_ciudad,
               c.departamento       AS cliente_departamento,
               c.cod_municipio      AS cliente_cod_municipio,
               c.tipo_persona,
               c.regimen_tributario AS cliente_regimen,
               u.nombre             AS usuario_nombre,
               e.nombre             AS empresa_nombre,
               e.nit                AS empresa_nit,
               e.dv                 AS empresa_dv,
               e.direccion          AS empresa_direccion,
               e.ciudad             AS empresa_ciudad,
               e.telefono           AS empresa_telefono,
               e.correo             AS empresa_correo,
               e.website            AS empresa_website,
               e.regimen_tributario AS empresa_regimen,
               e.actividad_economica,
               e.tarifa_ica         AS empresa_tarifa_ica,
               e.autoretenedor      AS empresa_autoretenedor,
               e.gran_contribuyente AS empresa_gran_contribuyente,
               e.prefijo_factura    AS empresa_prefijo,
               e.resolucion_dian    AS empresa_resolucion_dian,
               e.resolucion_fecha_desde AS empresa_resolucion_fecha_desde,
               e.resolucion_fecha_hasta AS empresa_resolucion_fecha_hasta,
               e.resolucion_desde   AS empresa_resolucion_desde,
               e.resolucion_hasta   AS empresa_resolucion_hasta,
               e.cod_municipio      AS empresa_cod_municipio,
               mp.descripcion       AS metodo_pago_nombre,
               pf.status            AS estado_pago
        FROM facturas f
            LEFT JOIN customers c     ON f.cod_cliente     = c.customer_id
            LEFT JOIN usuarios u      ON f.cod_usuario     = u.cod_usuario
            LEFT JOIN empresas e      ON f.cod_empresa     = e.cod_empresa
            LEFT JOIN metodos_pago mp ON f.cod_metodo_pago = mp.cod_pago
            LEFT JOIN pagos_factura pf ON f.cod_pago       = pf.cod_pago_factura
        WHERE f.cod_factura = %s
    """, (invoice_id,))


def get_invoice_details(invoice_id: int):
    return get_many("""
        SELECT d.*,
               p.nombre    AS producto_nombre,
               p.sku,
               p.tipo_item,
               p.unidad_medida,
               i.descripcion AS impuesto_nombre,
               i.codigo_dian AS impuesto_codigo_dian
        FROM detalle_factura d
            LEFT JOIN productos p  ON d.cod_producto  = p.cod_producto
            LEFT JOIN impuestos i  ON p.cod_impuesto  = i.cod_impuesto
        WHERE d.cod_factura = %s
        ORDER BY d.cod_destalle
    """, (invoice_id,))


def create_invoice(cod_cliente: int, cod_usuario: int, cod_empresa: int,
                   cod_metodo_pago: int, cod_pago: int, fecha: str,
                   total: float, subtotal: float, total_descuentos: float,
                   total_impuestos: float, tipo_factura: str = 'FV',
                   observaciones: str = '', fecha_vencimiento: str = None,
                   cufe: str = None, numero_factura: str = None,
                   forma_pago: str = 'CONTADO', orden_compra: str = None,
                   nombre_vendedor: str = None, cod_descuento_factura: int = None,
                   descripcion_descuento_factura: str = None):
    query = """
        INSERT INTO facturas
            (fecha, fecha_vencimiento, cod_cliente, cod_usuario, cod_empresa,
             cod_metodo_pago, cod_pago, total, subtotal, total_descuentos,
             total_impuestos, tipo_factura, observaciones,
             cufe, numero_factura, forma_pago, orden_compra, nombre_vendedor,
             cod_descuento_factura, descripcion_descuento_factura)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        fecha, fecha_vencimiento or None, cod_cliente, cod_usuario, cod_empresa,
        cod_metodo_pago, cod_pago, total, subtotal, total_descuentos,
        total_impuestos, tipo_factura, observaciones or None,
        cufe, numero_factura, forma_pago, orden_compra or None, nombre_vendedor or None,
        cod_descuento_factura or None, descripcion_descuento_factura or None
    ))


def create_invoice_detail(cod_factura: int, cod_producto: int, cantidad: int,
                           precio_unitario: float, subtotal: float,
                           descuento_porcentaje: float = 0, descuento_valor: float = 0,
                           descuento_descripcion: str = None,
                           impuesto_porcentaje: float = 0, impuesto_valor: float = 0):
    query = """
        INSERT INTO detalle_factura
            (cod_factura, cod_producto, cantidad, precio_unitario, subtotal,
             descuento_porcentaje, descuento_valor, descripcion_descuento,
             impuesto_porcentaje, impuesto_valor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        cod_factura, cod_producto, cantidad, precio_unitario, subtotal,
        descuento_porcentaje, descuento_valor, descuento_descripcion or None,
        impuesto_porcentaje, impuesto_valor
    ))


def get_notas_by_referencia(cod_factura_referencia: int):
    return get_many("""
        SELECT f.cod_factura, f.numero_factura, f.tipo_factura, f.fecha,
               f.total, f.motivo_nota, pf.status AS estado_pago
        FROM facturas f
            LEFT JOIN pagos_factura pf ON f.cod_pago = pf.cod_pago_factura
        WHERE f.cod_factura_referencia = %s
        ORDER BY f.fecha DESC
    """, (cod_factura_referencia,))


def update_invoice_status(invoice_id: int, cod_pago: int):
    return execute_update(
        "UPDATE facturas SET cod_pago = %s WHERE cod_factura = %s",
        (cod_pago, invoice_id)
    )


def delete_invoice(invoice_id: int):
    execute_update("DELETE FROM detalle_factura WHERE cod_factura = %s", (invoice_id,))
    execute_update("DELETE FROM factura_impuesto WHERE cod_factura = %s", (invoice_id,))
    execute_update("DELETE FROM factura_descuento WHERE cod_factura = %s", (invoice_id,))
    return execute_update("DELETE FROM facturas WHERE cod_factura = %s", (invoice_id,))


def get_dashboard_stats():
    stats = {}

    row = get_one("SELECT COUNT(*) AS total FROM facturas WHERE tipo_factura = 'FV'")
    stats['total_facturas'] = row['total'] if row else 0

    row = get_one("SELECT COALESCE(SUM(total), 0) AS total FROM facturas WHERE cod_pago = 1 AND tipo_factura='FV'")
    stats['ingresos_cobrados'] = row['total'] if row else 0

    row = get_one("SELECT COUNT(*) AS total FROM customers")
    stats['total_clientes'] = row['total'] if row else 0

    row = get_one("SELECT COUNT(*) AS total FROM productos WHERE activo = 1")
    stats['productos_activos'] = row['total'] if row else 0

    row = get_one("SELECT COALESCE(SUM(total),0) AS total FROM facturas WHERE cod_pago=2 AND tipo_factura='FV'")
    stats['facturas_pendientes'] = row['total'] if row else 0

    row = get_one("SELECT COUNT(*) AS total FROM productos WHERE stock <= stock_minimo AND activo=1")
    stats['productos_bajo_stock'] = row['total'] if row else 0

    stats['facturas_recientes'] = get_many("""
        SELECT f.cod_factura, f.fecha, f.total, f.tipo_factura,
               c.full_name AS cliente,
               pf.status AS estado_pago
        FROM facturas f
            LEFT JOIN customers c     ON f.cod_cliente = c.customer_id
            LEFT JOIN pagos_factura pf ON f.cod_pago   = pf.cod_pago_factura
        ORDER BY f.fecha DESC LIMIT 8
    """)
    return stats
