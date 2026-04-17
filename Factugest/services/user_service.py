from database import get_all_from_table, execute_query, execute_update, get_one
from auth import hash_password


def get_all_users():
    from database import get_many
    return get_many(
        "SELECT u.*, e.nombre AS empresa_nombre "
        "FROM usuarios u LEFT JOIN empresas e ON u.cod_empresa = e.cod_empresa "
        "ORDER BY u.nombre"
    )


def get_user_by_id(user_id: int):
    return get_one(
        "SELECT u.*, e.nombre AS empresa_nombre "
        "FROM usuarios u LEFT JOIN empresas e ON u.cod_empresa = e.cod_empresa "
        "WHERE u.cod_usuario = %s",
        (user_id,)
    )


def get_user_by_email(correo: str):
    return get_one(
        "SELECT u.*, e.nombre AS empresa_nombre "
        "FROM usuarios u LEFT JOIN empresas e ON u.cod_empresa = e.cod_empresa "
        "WHERE u.correo = %s",
        (correo,)
    )


def create_user(nombre: str, correo: str, contrasena: str, rol: str, cod_empresa: int = None):
    hashed = hash_password(contrasena)
    query = "INSERT INTO usuarios (nombre, correo, contrasena, rol, cod_empresa) VALUES (%s, %s, %s, %s, %s)"
    return execute_query(query, (nombre, correo, hashed, rol, cod_empresa))


def update_user(user_id: int, nombre: str, correo: str, rol: str, contrasena: str = None, cod_empresa: int = None):
    if contrasena:
        hashed = hash_password(contrasena)
        query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s, contrasena=%s, cod_empresa=%s WHERE cod_usuario=%s"
        return execute_update(query, (nombre, correo, rol, hashed, cod_empresa, user_id))
    else:
        query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s, cod_empresa=%s WHERE cod_usuario=%s"
        return execute_update(query, (nombre, correo, rol, cod_empresa, user_id))


def delete_user(user_id: int):
    return execute_update("DELETE FROM usuarios WHERE cod_usuario = %s", (user_id,))
