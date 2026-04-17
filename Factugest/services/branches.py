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
                  actividad_economica: str = "", tipo_documento: str = "NIT"):
    # Obtener nombre de ciudad para campo legacy ciudad
    ciudad = ""
    if cod_municipio:
        row = get_one("SELECT nombre FROM municipios WHERE cod_municipio = %s", (cod_municipio,))
        if row:
            ciudad = row["nombre"]
    query = """
        INSERT INTO empresas
            (nombre, nit, dv, direccion, ciudad, telefono, correo,
             regimen_tributario, actividad_economica, tipo_documento, cod_municipio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        nombre, nit, dv or None, direccion, ciudad, telefono, correo,
        regimen_tributario, actividad_economica or None, tipo_documento,
        cod_municipio or None
    ))


def update_branch(branch_id: int, nombre: str, nit: str, dv: str, direccion: str,
                  cod_municipio: str, telefono: str, correo: str,
                  regimen_tributario: str = "RESPONSABLE_IVA",
                  actividad_economica: str = "", tipo_documento: str = "NIT"):
    ciudad = ""
    if cod_municipio:
        row = get_one("SELECT nombre FROM municipios WHERE cod_municipio = %s", (cod_municipio,))
        if row:
            ciudad = row["nombre"]
    query = """
        UPDATE empresas
        SET nombre=%s, nit=%s, dv=%s, direccion=%s, ciudad=%s,
            telefono=%s, correo=%s, regimen_tributario=%s,
            actividad_economica=%s, tipo_documento=%s, cod_municipio=%s
        WHERE cod_empresa=%s
    """
    return execute_update(query, (
        nombre, nit, dv or None, direccion, ciudad, telefono, correo,
        regimen_tributario, actividad_economica or None, tipo_documento,
        cod_municipio or None, branch_id
    ))


def delete_branch(branch_id: int):
    return execute_update("DELETE FROM empresas WHERE cod_empresa = %s", (branch_id,))
