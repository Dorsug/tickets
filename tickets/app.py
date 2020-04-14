from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string, after_this_request, jsonify
import flask
import os.path
from os import mkdir
from . import db
from . import utils
from . import generate

from itertools import groupby, islice


def time_split(timedelta):
    return ":".join(str(timedelta).split(":")[0:2])


app = Flask("gestickets2", static_folder="assets")
app.teardown_appcontext(db.close_db)
app.jinja_env.filters["time_split"] = time_split
try:
    mkdir(app.instance_path)
except FileExistsError:
    pass
app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'tickets.sqlite'))
app.config.from_pyfile("config.default")


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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template(
            "index.html",
            ages=[x["interface"] for x in ages],
            heures=app.config["HORAIRES"],
            dates=app.config["DATES"],
            printers=app.config["IMPRIMANTES"],
        )


@app.route("/ateliers")
def ateliers():
    return generate.listerAtelier()


@app.route("/seances")
def seances():
    atelierId = request.values.get("atelierId")
    horaire = request.values.get("horaire")
    date = request.cookies.get("date")
    if atelierId:
        return generate.listerSeancesPourAtelier(atelierId, app.config["DATES"][date])
    elif horaire:
        return generate.listerSeancesPourHoraire(horaire, app.config["DATES"][date])


@app.route("/horaires")
def horaires():
    return generate.listerHoraires()


@app.route("/reservations")
def reservations():
    return generate.listerReservations()


@app.route("/panier", methods=["POST", "DELETE"])
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


@app.route("/panier", methods=["GET"])
def listerContenuPanier_cookie():
    panierId = request.cookies.get("panierId")
    if panierId is None:
        abort(400)
    return generate.listerPanier(panierId)


@app.route("/panier/<int:panierId>", methods=["GET"])
def listerContenuPanier_urlParam(panierId):
    return generate.listerPanier(panierId)


def impression(request, panierId):
    try:
        imprimante = request.cookies["imprimante"]
    except KeyError:
        imprimante = "1"  # Défaut de l'interface

    utils.impressionEtiquettes(panierId, imprimante)


@app.route("/paiement", methods=["POST"])
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


@app.route("/impression", methods=["POST"])
def route_impression():
    try:
        panierId = request.values.get("panierId")
    except KeyError:
        abort(400)
    impression(request, panierId)
    return flask.redirect(flask.url_for("index"))


@app.route("/panier/<int:panierId>")
def panierPrecedent(panierId):
    c = db.get_cursor()
    panier = db.callproc(c, "afficherContenuPanier", panierId)
    return render_template("panierPrecedent.html", panier=panier)


@app.route("/dispo/<string:date>")
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
            "dispo.html", seances=seancesTriees, horaires=app.config["HORAIRES"]
        )
