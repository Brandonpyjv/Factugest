from flask import render_template, Blueprint
from services.user_service import get_all_users

users_bp= Blueprint('users', __name__)

@users_bp.route('/users')
def users():
    data = get_all_users()
    return render_template('users/index.html', usuarios=data)

@users_bp.route('/users/new')
def new_user():
    return render_template('users/form.html')