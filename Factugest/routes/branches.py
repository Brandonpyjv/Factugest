from flask import render_template, Blueprint
from services.branches import get_all_branches

branches_bp = Blueprint('branches', __name__)


@branches_bp.route('/branches', endpoint='branches')
def branches():
    data=get_all_branches()
    return render_template('branches/index.html', branches=data)

@branches_bp.route('/new_branch')
def new_branch():
    return render_template('branches/form.html')

