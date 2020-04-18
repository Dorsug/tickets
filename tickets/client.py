from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string, after_this_request, jsonify
from flask import Blueprint, current_app
from flask import current_app as capp
import flask
from . import db
from . import utils

from itertools import groupby, islice

bp = Blueprint("client", __name__)


@bp.route("/", methods=["GET"])
def index():
    c = db.get_cursor()
    date = utils.get_date(request.cookies.get("date"))
    capp.logger.debug(f"{date=}")
    ateliers = c.execute('SELECT id, nom, numero, nombreplace FROM atelier').fetchall()
    ateliers = [dict(x) for x in ateliers]
    for atelier in ateliers:
        seances = c.execute('''SELECT seance.id, seance.datetime FROM seance
            WHERE seance.atelier = ?
            AND seance.datetime BETWEEN ? AND ?''',
            (atelier['id'], date + ' 00:00:00', date + ' 23:59:59')
        ).fetchall()
        atelier['seances'] = {x['datetime'].split(' ')[1]:dict(x) for x in seances}
    return render_template("index.html", horaires=utils.get_horaires(), ateliers=ateliers)


@bp.route("/reservations")
def reservations():
    return 'TODO'


@bp.route("/panier", methods=["POST", "DELETE"])
def panier():
    if request.method == "POST":
        seanceId = request.values.get("seanceId")
        if seanceId is None:
            abort(400)
        panierId = request.cookies.get("panierId")
        if panierId is None:
            panierId = db.Proc.nouveauPanier()
            capp.logger.debug(f"{panierId=}")
            @after_this_request
            def add_cookie(response):
                response.set_cookie("panierId", str(panierId))
                return response
        itemId = db.Proc.ajouterSeanceAuPanier(panierId, seanceId)
        return jsonify(itemId=itemId)

    elif request.method == "DELETE":
        panierId = request.cookies.get("panierId")
        seanceId = request.values.get("seanceId")
        if panierId is None:
            abort(400)
        if seanceId is None:  # Vider tout le panier
            utils.viderPanier(panierId)
        else:
            utils.enleverDuPanier(panierId, seanceId)
        return ""


@bp.route("/panier", methods=["GET"])
def listerContenuPanier_cookie():
    panierId = request.cookies.get("panierId")
    if panierId is None:
        abort(400)
    return 'TODO'


@bp.route("/panier/<int:panierId>", methods=["GET"])
def listerContenuPanier_urlParam(panierId):
    return 'TODO'


def impression(request, panierId):
    try:
        imprimante = request.cookies["imprimante"]
    except KeyError:
        imprimante = "1"  # Défaut de l'interface

    utils.impressionEtiquettes(panierId, imprimante)


@bp.route("/paiement", methods=["POST"])
def paiement():
    try:
        panierId = request.cookies["panierId"]
    except KeyError:  # Il n'y a pas de panier
        abort(400)

    impression(request, panierId)

    utils.payerPanier(
        panierId, request.form["modePaiement"], request.form["codePostal"]
    )

    @after_this_request
    def delete_cookie(response):
        # Expire dans le passé, donc immédiatement
        response.set_cookie("panierId", "", expires=0)
        return response

    return flask.redirect(flask.url_for("index"))


@bp.route("/impression", methods=["POST"])
def route_impression():
    try:
        panierId = request.values.get("panierId")
    except KeyError:
        abort(400)
    impression(request, panierId)
    return flask.redirect(flask.url_for("index"))


@bp.route("/panier/<int:panierId>")
def panierPrecedent(panierId):
    c = db.get_cursor()
    panier = db.callproc(c, "afficherContenuPanier", panierId)
    return render_template("panierPrecedent.html", panier=panier)


@bp.route("/dispo/<string:date>")
def dispo(date):
    c = db.get_cursor()
    seances = db.callproc(c, "listerPlacesDispo", date)

    seancesTriees = []
    for k, g in groupby(seances, lambda x: x["nom"]):
        l = [x["placesRestantes"] for x in g]
        seancesTriees.append((k, l))

    if request.headers["Accept"] == "application/json":
        return jsonify(seancesTriees)
    else:
        n = request.values.get("n")
        if n:
            seancesTriees = seancesTriees[: int(n)]
        return render_template(
            "dispo.html", seances=seancesTriees, horaires=current_app.config["HORAIRES"]
        )
