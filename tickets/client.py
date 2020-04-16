from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string, after_this_request, jsonify
from flask import Blueprint, current_app
import flask
from . import db
from . import utils
from . import generate

from itertools import groupby, islice

bp = Blueprint("client", __name__)

ages = [
    {"intv": [0, 99], "interface": "Tout Public"},
    {"intv": [0, 4], "interface": "0 - 4"},
    {"intv": [4, 6], "interface": "4 - 6"},
    {"intv": [6, 8], "interface": "6 - 8"},
    {"intv": [8, 10], "interface": "8 - 10"},
    {"intv": [10, 12], "interface": "10 - 12"},
    {"intv": [12, 14], "interface": "12 - 14"},
    {"intv": [14, 18], "interface": "14 - 18"},
]


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template(
            "index.html",
            ages=[x["interface"] for x in ages]
        )
            # heures=current_app.config["HORAIRES"],
            # printers=current_app.config["IMPRIMANTES"],
            # dates=current_app.config["DATES"],


@bp.route("/ateliers")
def ateliers():
    return generate.listerAtelier()


@bp.route("/seances")
def seances():
    atelierId = request.values.get("atelierId")
    horaire = request.values.get("horaire")
    date = request.cookies.get("date")
    if atelierId:
        return generate.listerSeancesPourAtelier(atelierId, current_app.config["DATES"][date])
    elif horaire:
        return generate.listerSeancesPourHoraire(horaire, current_app.config["DATES"][date])


@bp.route("/horaires")
def horaires():
    return generate.listerHoraires()


@bp.route("/reservations")
def reservations():
    return generate.listerReservations()


@bp.route("/panier", methods=["POST", "DELETE"])
def panier():
    if request.method == "POST":
        seanceId = request.values.get("seanceId")
        if seanceId is None:
            abort(400)
        panierId = request.cookies.get("panierId")
        resp = flask.make_response("Ok")
        if panierId is None:
            panierId = utils.nouveauPanier()
            resp.set_cookie("panierId", panierId)
        utils.ajouterSeanceAuPanier(panierId, seanceId)
        return resp
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
    return generate.listerPanier(panierId)


@bp.route("/panier/<int:panierId>", methods=["GET"])
def listerContenuPanier_urlParam(panierId):
    return generate.listerPanier(panierId)


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
