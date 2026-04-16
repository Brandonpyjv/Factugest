from database import get_all_from_table, execute_query, execute_update, get_one
from auth import hash_password


def get_all_users():
    return get_all_from_table("usuarios")


def get_user_by_id(user_id: int):
    return get_one("SELECT * FROM usuarios WHERE cod_usuario = %s", (user_id,))


def get_user_by_email(correo: str):
    return get_one("SELECT * FROM usuarios WHERE correo = %s", (correo,))


def create_user(nombre: str, correo: str, contrasena: str, rol: str):
    hashed = hash_password(contrasena)
    query = "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (nombre, correo, hashed, rol))


def update_user(user_id: int, nombre: str, correo: str, rol: str, contrasena: str = None):
    if contrasena:
        hashed = hash_password(contrasena)
        query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s, contrasena=%s WHERE cod_usuario=%s"
        return execute_update(query, (nombre, correo, rol, hashed, user_id))
    else:
        query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s WHERE cod_usuario=%s"
        return execute_update(query, (nombre, correo, rol, user_id))


def delete_user(user_id: int):
    return execute_update("DELETE FROM usuarios WHERE cod_usuario = %s", (user_id,))
