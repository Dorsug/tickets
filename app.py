from flask import Flask, render_template, request
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
    else:
        results = db.callproc(c, 'listerSeancesPourAtelier', id)
    for seance in results:
        html += f"""
            <p style="cursor: pointer;background-color: #777;border-radius: 5px;">
                <strong>{ seance['Date'] }</strong><br />
                { seance['Heure debut'] } - { seance['Heure fin'] }<br />
                Atelier { seance['Numero atelier'] }
            </p>
        """
    return html
