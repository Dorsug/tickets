from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string, after_this_request, jsonify
from flask import Blueprint, current_app
from flask import current_app as capp
import flask
from . import db
from . import utils
import sqlite3

from itertools import groupby, islice

bp = Blueprint("client", __name__)


@bp.route("/", methods=["GET"])
def index():
    cur = db.get_cursor()
    date = utils.get_date(request.cookies.get("date"))
    capp.logger.debug(f"{date=}")
    ateliers = db.select('SELECT id, nom, numero, pole, nombreplace FROM atelier', cur=cur)
    poles = db.select('SELECT id, nom, couleur FROM pole', cur=cur)
    for atelier in ateliers:
        seances = db.select('''
            SELECT
                Seance.id,
                TIME(Seance.datetime) AS horaire,
                (SELECT COUNT(ItemPanier.id)
                    FROM ItemPanier
                    WHERE ItemPanier.seance = Seance.id
                ) AS placesPrises
            FROM seance
            WHERE seance.atelier = ?
            AND seance.datetime BETWEEN ? AND ?''',
            (atelier['id'], date + ' 00:00:00', date + ' 23:59:59'), cur=cur)
        for seance in seances:
            seance['placesRestantes'] = atelier['nombreplace'] - seance['placesPrises']
            del seance['placesPrises']
        atelier['seances'] = {utils.ptime(x['horaire']):dict(x) for x in seances}
    return render_template("index.html", horaires=utils.get_horaires(), ateliers=ateliers, poles=poles)


@bp.route("/reservations")
def reservations():
    return 'TODO'


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
