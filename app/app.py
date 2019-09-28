from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string
from . import db
from . import utils
from . import generate


app = Flask('gestickets2', static_folder='assets')
app.teardown_appcontext(db.close_db)


@app.route('/')
def index():
    c = db.get_cursor()
    ateliers = db.callproc(c, 'listerAtelier')
    ages = ['Tout Public',
            '0 - 4',
            '4 - 6',
            '6 - 8',
            '8 - 10',
            '10 - 12',
            '12 - 14',
            '14 - 18'
            ]
    return render_template('index.html', ateliers=ateliers, ages=ages)


@app.route('/ateliers')
def ateliers():
    return generate.listerAtelier()


@app.route('/seances')
def seances():
    atelierId = request.values.get('atelierId')
    return generate.listerSeancesPourAtelier(atelierId)


@app.route('/horaires')
def horaires():
    return generate.listerHoraires()


@app.route('/panier', methods=['GET', 'POST', 'DELETE'])
def panier():
    if request.method == 'GET':
        action = request.values.get('action')
        if action == 'new':
            return utils.nouveauPanier()
        if action == 'lister':
            panierId = request.cookies.get('panierId')
            if panierId is None:
                abort(400)
            return generate.listerPanier(panierId)
        else:
            abort(404)
    elif request.method == 'POST':
        seanceId = request.values.get('seanceId')
        if seanceId is None:
            abort(400)
        panierId = request.cookies.get('panierId')
        if panierId is None:
            panierId = utils.nouveauPanier()
        utils.ajouterSeanceAuPanier(panierId, seanceId)
        return panierId
    elif request.method == 'DELETE':
        panierId = request.cookies.get('panierId')
        seanceId = request.values.get('seanceId')
        if panierId is None:
            abort(400)
        if seanceId is None: # Vider tout le panier
            utils.viderPanier(panierId)
        else:
            utils.enleverDuPanier(panierId, seanceId)
        return ''
    else:
        abort(404)


@app.route('/paiement', methods=['POST'])
def paiement():
    # TODO Voir ou stocker modePaiement et codePostal
    # print(request.form)

    try:
        panierId = request.cookies['panierId']
    except KeyError: # Il n'y a pas de panier
        abort(400)
    utils.marquePanierPaye(panierId)

    utils.impressionEtiquettes(panierId)

    # Supprime id du panier validé ét redirige vers la page principale
    return render_template('paiement.html')
