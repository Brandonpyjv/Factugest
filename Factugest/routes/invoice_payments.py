from flask import render_template, Blueprint
from services.invoice_payments_service import get_all_invoice_payments

invoice_payments_bp = Blueprint('invoice_payments', __name__)

@invoice_payments_bp.route("/invoice_payments", endpoint='invoice_payments')
def invoice_payments():
    data = get_all_invoice_payments()
    return render_template("invoice_payments/index.html", all_invoices=data)

@invoice_payments_bp.route("/invoice_payments/new", endpoint="/invoice_payments/new")
def product_discounts():
    return render_template("invoice_payments/form.html")