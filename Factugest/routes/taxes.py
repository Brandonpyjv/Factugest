from flask import render_template, Blueprint
from services.taxes import get_all_invoice_taxes


invoice_taxes_bp = Blueprint('taxes', __name__)


@invoice_taxes_bp.route('/invoice_taxes', endpoint='invoice_taxes')
def invoice_taxes():
    data=get_all_invoice_taxes()
    return render_template('invoice_taxes/index.html', invoice_taxes=data)


@invoice_taxes_bp.route("/taxes/new", endpoint="taxes/new")
def logs():
    return render_template("invoice_taxes/form.html")