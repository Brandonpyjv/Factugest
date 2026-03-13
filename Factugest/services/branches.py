from database import get_all_from_table, execute_query, execute_update, get_one, get_many


def get_all_branches():
    return get_many("SELECT * FROM empresas ORDER BY nombre")


def get_branch_by_id(branch_id: int):
    return get_one("SELECT * FROM empresas WHERE cod_empresa = %s", (branch_id,))


def create_branch(nombre: str, nit: str, dv: str, direccion: str, ciudad: str,
                  telefono: str, correo: str, regimen_tributario: str = "RESPONSABLE_IVA",
                  actividad_economica: str = "", tipo_documento: str = "NIT"):
    query = """
        INSERT INTO empresas
            (nombre, nit, dv, direccion, ciudad, telefono, correo,
             regimen_tributario, actividad_economica, tipo_documento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (
        nombre, nit, dv or None, direccion, ciudad, telefono, correo,
        regimen_tributario, actividad_economica or None, tipo_documento
    ))


def update_branch(branch_id: int, nombre: str, nit: str, dv: str, direccion: str,
                  ciudad: str, telefono: str, correo: str,
                  regimen_tributario: str = "RESPONSABLE_IVA",
                  actividad_economica: str = "", tipo_documento: str = "NIT"):
    query = """
        UPDATE empresas
        SET nombre=%s, nit=%s, dv=%s, direccion=%s, ciudad=%s,
            telefono=%s, correo=%s, regimen_tributario=%s,
            actividad_economica=%s, tipo_documento=%s
        WHERE cod_empresa=%s
    """
    return execute_update(query, (
        nombre, nit, dv or None, direccion, ciudad, telefono, correo,
        regimen_tributario, actividad_economica or None, tipo_documento, branch_id
    ))


def delete_branch(branch_id: int):
    return execute_update("DELETE FROM empresas WHERE cod_empresa = %s", (branch_id,))
