from database import get_all_from_table

def get_all_invoice_payments():
    return get_all_from_table('pagos_factura')


