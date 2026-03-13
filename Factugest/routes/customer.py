from flask import render_template, Blueprint
from services.customer_service import get_all_customers

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customer', endpoint='customer')
def customer():
    data=get_all_customers()
    return render_template('customer/index.html', all_customers=data)

@customer_bp.route('/new_customer', endpoint='new_customer')
def new_customer():
    return render_template('customer/form.html')