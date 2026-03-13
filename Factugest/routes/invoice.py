from flask import render_template, Blueprint
from services.invoice_service import get_all_invoices_detailed

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/invoice', endpoint='invoice')
def invoice():
    data=get_all_invoices_detailed()
    return render_template('invoice/index.html', all_invoices=data)

@invoice_bp.route('/new_invoice', endpoint='new_invoice')
def new_invoice():
    return render_template('invoice/form.html')
