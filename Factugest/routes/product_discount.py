from flask import Blueprint, render_template
from services.product_discount_service import get_all_product_discounts

product_discount_bp = Blueprint('product_discount', __name__)


@product_discount_bp.route('/product_discounts', endpoint='product_discounts')
def product_discounts():
    data = get_all_product_discounts()
    return render_template('product_discounts/index.html', all_product_discounts=data)


@product_discount_bp.route('/new_product_discounts', endpoint='new_product_discounts')
def nee_product_discounts():
    return render_template('product_discounts/form.html')