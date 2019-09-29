from flask import Flask, render_template, request, abort, redirect
from flask import render_template_string
from . import db
from . import utils
from . import generate


app = Flask('gestickets2', static_folder='assets')
app.teardown_appcontext(db.close_db)

ages = [
        {'intv': [0, 99], 'interface': 'Tout Public'},
        {'intv': [0, 4], 'interface': '0 - 4'},
        {'intv': [4, 6], 'interface': '4 - 6'},
        {'intv': [6, 8], 'interface': '6 - 8'},
        {'intv': [8, 10], 'interface': '8 - 10'},
        {'intv': [10, 12], 'interface': '10 - 12'},
        {'intv': [12, 14], 'interface':'12 - 14'},
        {'intv': [14, 18], 'interface': '14 - 18'}
        ]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        c = db.get_cursor()
        ateliers = db.callproc(c, 'listerAtelier')
        return render_template(
            'index.html',
            ateliers=ateliers,
            ages=[x['interface'] for x in ages]
        )
    if request.method == 'POST':
        data = request.get_json()

        ages_ns = [int(x) for x in data['age']]
        ages_in = []
        for age_n in ages_ns:
            ages_in.extend(ages[age_n - 1]['intv'])
        if ages_in != []:
            age_maxi = max(ages_in)
            age_mini = min(ages_in)
        else:
            age_maxi = None
            age_mini = None

        atelier = ','.join(data['atelier'])

        c = db.get_cursor()
        ateliers = db.callproc(c, 'listerSeancePourFiltres', atelier, None, age_mini, age_maxi)
        return render_template('ateliers.html', ateliers=ateliers)


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