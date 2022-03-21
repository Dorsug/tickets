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
    natural_date = request.cookies.get("date")
    date = utils.get_date(natural_date)
    poles, ateliers, seances = db.Proc.listerSeancesEtAteliers(date)
    return render_template(
        "index.html",
        horaires=utils.get_horaires(),
        ateliers=ateliers,
        poles=poles,
        admin=(True if "admin" in request.args else False),
        natural_date=natural_date,
        date=date,
        imprimante=request.cookies.get('imprimante'),
        panierId=request.cookies.get('panierId'),
    )


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
    db.Proc.markPrinted(panierId)


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
@bp.route("/impression/<int:panierId>", methods=["POST"])
def route_impression(panierId=None):
    if panierId is None:
        try:
            panierId = request.values.get("panierId")
        except KeyError:
            abort(400)
    impression(request, panierId)
    return 'Done'

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
        panierId=request.cookies.get('panierId'),
        admin=(True if "admin" in request.args else False),
    )

@bp.route("/historique", methods=["GET"])
def historique():
    c = db.get_cursor()
    paniers, seances = db.Proc.historique(cur=c)
    return render_template(
        "historique.html",
        paniers=paniers,
        seances=seances,
        natural_date=request.cookies.get("date"),
        imprimante=request.cookies.get('imprimante'),
        panierId=request.cookies.get('panierId'),
        admin=(True if "admin" in request.args else False),
    )


@bp.route("/dispo/<string:date>")
def dispo(date):
    natural_date = request.cookies.get("date")
    date = utils.get_date(natural_date)
    poles, ateliers, seances = db.Proc.listerSeancesEtAteliers(date)

    nbAteliersPage = 10
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 0

    return render_template("dispo.html",
        horaires=utils.get_horaires(),
        ateliers=ateliers[page * nbAteliersPage:(page + 1) * nbAteliersPage],
        poles=poles,
        natural_date=natural_date,
        date=date,
    )
