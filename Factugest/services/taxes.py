from database import get_all_from_table

def get_all_invoice_taxes():
    return get_all_from_table('impuestos')