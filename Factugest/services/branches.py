from database import get_all_from_table, execute_query, execute_update, get_one, get_many


def get_all_branches():
    return get_many("""
        SELECT e.*, m.nombre AS municipio_nombre, d.nombre AS departamento_nombre,
               m.cod_departamento
        FROM empresas e
        LEFT JOIN municipios m ON e.cod_municipio = m.cod_municipio
        LEFT JOIN departamentos d ON m.cod_departamento = d.cod_departamento
        ORDER BY e.nombre
    """)


def get_branch_by_id(branch_id: int):
    return get_one("""
        SELECT e.*, m.nombre AS municipio_nombre, d.nombre AS departamento_nombre,
               m.cod_departamento
        FROM empresas e
        LEFT JOIN municipios m ON e.cod_municipio = m.cod_municipio
        LEFT JOIN departamentos d ON m.cod_departamento = d.cod_departamento
        WHERE e.cod_empresa = %s
    """, (branch_id,))


def create_branch(nombre: str, nit: str, dv: str, direccion: str, cod_municipio: str,
                  telefono: str, correo: str, regimen_tributario: str = "RESPONSABLE_IVA",
                  actividad_economica: str = "", tipo_documento: str = "NIT",
                  website: str = "", tarifa_ica: str = "", autoretenedor: int = 0,
                  gran_contribuyente: int = 0, prefijo_factura: str = "FV",
                  resolucion_dian: str = "", resolucion_fecha_desde: str = None,
                  resolucion_fecha_hasta: str = None, resolucion_desde: int = None,
                  resolucion_hasta: int = None, consecutivo_actual: int = 1):
    ciudad = ""
    if cod_municipio:
        row = get_one("SELECT nombre FROM municipios WHERE cod_municipio = %s", (cod_municipio,))
        if row:
            ciudad = row["nombre"]
    query = """
        INSERT INTO empresas
            (nombre, nit, dv, direccion, ciudad, telefono, correo,
             regimen_tributario, actividad_economica, tipo_documento, cod_municipio,
             website, tarifa_ica, autoretenedor, gran_contribuyente,
             prefijo_factura, resolucion_dian, resolucion_fecha_desde,
             resolucion_fecha_hasta, resolucion_desde, resolucion_hasta, consecutivo_actual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        nombre, nit, dv or None, direccion, ciudad, telefono, correo,
        regimen_tributario, actividad_economica or None, tipo_documento,
        cod_municipio or None, website or None, tarifa_ica or None,
        autoretenedor, gran_contribuyente, prefijo_factura or 'FV',
        resolucion_dian or None, resolucion_fecha_desde or None,
        resolucion_fecha_hasta or None, resolucion_desde or None,
        resolucion_hasta or None, consecutivo_actual or 1
    ))


def update_branch(branch_id: int, nombre: str, nit: str, dv: str, direccion: str,
                  cod_municipio: str, telefono: str, correo: str,
                  regimen_tributario: str = "RESPONSABLE_IVA",
                  actividad_economica: str = "", tipo_documento: str = "NIT",
                  website: str = "", tarifa_ica: str = "", autoretenedor: int = 0,
                  gran_contribuyente: int = 0, prefijo_factura: str = "FV",
                  resolucion_dian: str = "", resolucion_fecha_desde: str = None,
                  resolucion_fecha_hasta: str = None, resolucion_desde: int = None,
                  resolucion_hasta: int = None, consecutivo_actual: int = 1):
    ciudad = ""
    if cod_municipio:
        row = get_one("SELECT nombre FROM municipios WHERE cod_municipio = %s", (cod_municipio,))
        if row:
            ciudad = row["nombre"]
    query = """
        UPDATE empresas
        SET nombre=%s, nit=%s, dv=%s, direccion=%s, ciudad=%s,
            telefono=%s, correo=%s, regimen_tributario=%s,
            actividad_economica=%s, tipo_documento=%s, cod_municipio=%s,
            website=%s, tarifa_ica=%s, autoretenedor=%s, gran_contribuyente=%s,
            prefijo_factura=%s, resolucion_dian=%s, resolucion_fecha_desde=%s,
            resolucion_fecha_hasta=%s, resolucion_desde=%s, resolucion_hasta=%s,
            consecutivo_actual=%s
        WHERE cod_empresa=%s
    """
    return execute_update(query, (
        nombre, nit, dv or None, direccion, ciudad, telefono, correo,
        regimen_tributario, actividad_economica or None, tipo_documento,
        cod_municipio or None, website or None, tarifa_ica or None,
        autoretenedor, gran_contribuyente, prefijo_factura or 'FV',
        resolucion_dian or None, resolucion_fecha_desde or None,
        resolucion_fecha_hasta or None, resolucion_desde or None,
        resolucion_hasta or None, consecutivo_actual or 1, branch_id
    ))


def delete_branch(branch_id: int):
    return execute_update("DELETE FROM empresas WHERE cod_empresa = %s", (branch_id,))
