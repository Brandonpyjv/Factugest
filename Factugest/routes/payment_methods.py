from flask import render_template, Blueprint
from services.payment_methods_service import get_all_payment_methods

payment_methods_bp = Blueprint('payment_methods',__name__)


@payment_methods_bp.route('/payment_methods', endpoint='payment_methods')
def payment_methods():
    data=get_all_payment_methods()
    return render_template("payment_methods/index.html", all_payment_methods=data)
    

@payment_methods_bp.route("/payment_methods/new", endpoint="/payment_methods/new")
def payment_methods_new():
    return render_template("payment_methods/form.html")

