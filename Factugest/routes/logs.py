
from flask import render_template, Blueprint
from services.logs_service import get_all_logs


logs_bp = Blueprint('logs', __name__)



@logs_bp.route("/logs", endpoint='logs')
def logs():
    data=get_all_logs()
    return render_template("logs/index.html", logs=data )
