from flask import render_template, Blueprint
from services.products_service import get_all_products_detailed

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route("/product", endpoint='product')
def products():
    data=get_all_products_detailed()
    return render_template("product/index.html", products=data)

@products_bp.route('/product/new', endpoint='product/new')
def product_new():
    return render_template('product/form.html')

