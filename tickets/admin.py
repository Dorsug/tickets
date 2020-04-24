from flask import Blueprint

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
def index():
    return 'hello world'
