from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string, after_this_request, jsonify
from flask import Blueprint, current_app
from flask import current_app as capp
import flask
from . import db
from . import utils
import sqlite3
import math

from itertools import groupby, islice

bp = Blueprint("client", __name__)


@bp.route("/", methods=["GET"])
def index():
    cur = db.get_cursor()
    imprimante = request.cookies.get('imprimante')
    natural_date = request.cookies.get("date")
    date = utils.get_date(natural_date)
    ateliers = db.select('SELECT id, nom, numero, pole, nombreplace, description FROM atelier', cur=cur)
    poles = db.select('SELECT id, nom, couleur FROM pole', cur=cur)
    for atelier in ateliers:
        seances = db.select('''
            SELECT
                Seance.id,
                Seance.datetime,
                (SELECT COUNT(ItemPanier.id)
                    FROM ItemPanier
                    WHERE ItemPanier.seance = Seance.id
                ) AS placesPrises
            FROM seance
            WHERE seance.atelier = ?
            AND DATE(seance.datetime) = ?''',
            (atelier['id'], date), cur=cur)
        for seance in seances:
            seance['placesRestantes'] = atelier['nombreplace'] - seance['placesPrises']
            del seance['placesPrises']
        atelier['seances'] = {x['datetime']:dict(x) for x in seances}
    return render_template("index.html", horaires=utils.get_horaires(), ateliers=ateliers, poles=poles, admin=(True if "admin" in request.args else False), natural_date=natural_date, date=date, imprimante=imprimante)


@bp.route("/panier", methods=["POST"])
def ajouterAupanier():
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
    try:
        itemId = db.Proc.ajouterSeanceAuPanier(panierId, seanceId)
    except sqlite3.IntegrityError as e:
        if e.args[0] == 'SeanceFull':
            abort(410) # HTTP code: Gone
        else:
            raise
    return jsonify(itemId=itemId)


@bp.route("/panier", methods=["DELETE"])
def enleverDuPanier():
    itemId = request.values.get("itemId")
    if itemId is None:  # Vider tout le panier
        panierId = request.cookies.get("panierId")
        if panierId is None:
            abort(400)
        db.Proc.viderPanier(panierId)
    else:
        db.Proc.enleverDuPanier(itemId)
    return jsonify(success=True)


@bp.route("/panier", methods=["GET"])
def listerContenuPanier():
    panierId = request.values.get("q", request.cookies.get("panierId"))
    if panierId is None:
        abort(400)
    items = db.Proc.listerContenuPanier(panierId)
    for item in items:
        item['datetime'] = utils.get_naturalDatetime(item['datetime'])
    return jsonify(items)


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


@bp.route("/reserver", methods=["POST"])
def reserver():
    try:
        panierId = request.cookies["panierId"]
    except KeyError:  # Il n'y a pas de panier
        abort(400)

    utils.reserver(
        panierId, *[request.form[key] for key in ["nom", "prenom", "email", "modePaiement", "codePostal"]],
    )

    @after_this_request
    def delete_cookie(response):
        # Expire dans le passé, donc immédiatement
        response.set_cookie("panierId", "", expires=0)
        return response

    return flask.redirect(flask.url_for("index", admin=True))


@bp.route("/impression", methods=["POST"])
def route_impression():
    try:
        panierId = request.values.get("panierId")
    except KeyError:
        abort(400)
    impression(request, panierId)
    return flask.redirect(flask.url_for("index"))

@bp.route("/reservations", methods=["GET"])
def reservations():
    c = db.get_cursor()
    clients, seances = db.Proc.listerReservations(c)
    return render_template(
        "reservations.html",
        clients=clients,
        seances=seances,
        natural_date=request.cookies.get("date"),
        imprimante=request.cookies.get('imprimante'),
    )


HORAIRES = [
    '10:30',
    '11:30',
    '14:00',
    '15:00',
    '16:00',
    '17:00',
    '18:00'
]

@bp.route("/dispo/<string:date>")
def dispo(date):
    c = db.get_cursor()
    seances = db.Proc.listerPlacesDispo(date, c)

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
            "dispo.html", seances=seancesTriees, horaires=HORAIRES
        )
