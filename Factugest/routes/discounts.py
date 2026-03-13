from flask import render_template, Blueprint
from services.discounts import get_all_discount

discount_bp = Blueprint('discount', __name__)


@discount_bp.route('/discount', endpoint='discount')
def discount(): 
    data=get_all_discount()
    return render_template('discount/index.html',all_discount=data)

@discount_bp.route('/new_discount', endpoint='new_discount')
def new_discount():
    return render_template('discount/form.html')