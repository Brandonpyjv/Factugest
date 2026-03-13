from database import get_all_from_table

def get_all_payment_methods():
    return get_all_from_table('metodos_pago')