from flask import Flask, render_template, request, abort
from flask import render_template_string
import db
import utils
from pprint import pprint

app = Flask(__name__, static_folder='assets')
app.teardown_appcontext(db.close_db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ateliers')
def ateliers():
    return utils.listerAtelier()


@app.route('/seances')
def seances():
    atelierId = request.values.get('atelierId')
    return utils.listerSeancesPourAtelier(atelierId)


@app.route('/horaires')
def horaires():
    return utils.listerSeances()


@app.route('/panier', methods=['GET', 'POST'])
def panier():
    if request.method == 'GET':
        action = request.values.get('action')
        if action == 'new':
            return utils.nouveauPanier()
        if action == 'lister':
            panierId = request.values.get('panierId')
            if panierId is None:
                abort(400)
            return utils.listerPanier(panierId)
        else:
            abort(404)
    elif request.method == 'POST':
        action = request.values.get('action')
        if action == 'ajouter':
            panierId = request.values.get('panierId')
            seanceId = request.values.get('seanceId')
            if panierId is None or seanceId is None:
                abort(400)
            return utils.ajouterSeanceAuPanier(panierId, seanceId)
        else:
            abort(404)
    else:
        abort(404)
