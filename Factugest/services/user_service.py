from database import get_all_from_table

def get_all_users():
    return get_all_from_table("usuarios")