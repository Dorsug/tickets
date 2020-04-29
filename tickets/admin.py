from flask import Blueprint, render_template, jsonify
from . import db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
def index():
    return render_template("admin.html")


@bp.route("/ateliers", methods=["GET"])
def ateliers():
    return jsonify(db.Proc.listerAtelier())
