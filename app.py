from flask import Flask, render_template, request, abort
import db
from pprint import pprint

app = Flask(__name__, static_folder='assets')
app.teardown_appcontext(db.close_db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ateliers')
def ateliers():
    html = ''
    c = db.get_cursor()
    results = db.callproc(c, 'listerAtelier')
    for atelier in results:
        html += f"""
            <p onclick="displaySession({ atelier['ID'] });" style="cursor: pointer;background-color: #999;border-radius: 5px;">
                <strong>{ atelier['Numero'] } - { atelier['Nom'] }</strong><br />
                { atelier['Description'] }<br />
                Age: { atelier['Age mini'] }  - { atelier['Age maxi'] }<br />
                { atelier['Prix'] }€
            </p>
        """
    return html


@app.route('/horaires')
def horaires():
    html = ''
    c = db.get_cursor()

    # Test si il y a un id en paramètre de la requete
    id = request.args.get('id')
    if not id:
        results = db.callproc(c, 'listerSeances')
        for seance in results:
            html += f"""
                <p style="cursor: pointer;background-color: #777;border-radius: 5px;">
                    <strong>{ seance['Date'] }</strong><br />
                    { seance['Heure debut'] } - { seance['Heure fin'] }<br />
                    Atelier { seance['Numero atelier'] }
                </p>
            """
    else:
        results = db.callproc(c, 'listerSeancesPourAtelier', id)
        for seance in results:
            html += f"""
                <p style="cursor: pointer;background-color: #777;border-radius: 5px;"
                onclick="ajouterSeanceAuPanier({ seance['ID'] });">
                    <strong>{ seance['Date'] }</strong><br />
                    { seance['Heure debut'] } - { seance['Heure fin'] }<br />
                    Places restantes: { seance['Places Dispo'] }
                </p>
            """
    return html


@app.route('/panier', methods=['GET', 'POST'])
def panier():
    print(f'request.method: { request.method }')
    if request.method == 'GET':
        action = request.args.get('action')
        print(f'action: {action}')
        # Créer un nouveau panier
        if action == 'new':
            c = db.get_cursor()
            panier = db.callproc(c, 'obtenirIdPanier', '@idPanier')[0]['out_id']
            return str(panier)
        if action == 'lister':
            panierId = request.values.get('panierId')
            if panierId is None:
                abort(400)
            c = db.get_cursor()
            panier = db.callproc(c, 'afficherContenuPanier', panierId)
            html = ''
            for seance in panier:
                html += f"""
                    <strong>{ seance['Numero atelier'] } - { seance['Nom atelier'] }</strong><br />
                    { seance['heureDebut'] } - { seance['heurefin'] }<br />
                    { seance['prix'] }
            """
            return html
        else:
            abort(404)
    elif request.method == 'POST':
        c = db.get_cursor()
        action = request.values.get('action')
        if action == 'ajouter':
            panierId = request.values.get('panierId')
            seanceId = request.values.get('seanceId')
            if panierId is None or seanceId is None:
                print(f'Requete manque paramètres {panierId, seanceId}')
                abort(400)
            result = db.callproc(c, 'ajouterSeanceAuPanier', panierId, seanceId, None, '@success')
            success = result[1][0]['out_result']
            print(success)
            return ''
        else:
            abort(404)
    else:
        abort(404)
