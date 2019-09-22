from flask import Flask, render_template, request, abort
from flask import render_template_string
import db


def listerAtelier():
    c = db.get_cursor()
    ateliers = db.callproc(c, 'listerAtelier')
    template = """
        {% for atelier in ateliers %}
        <p onclick="listerSeances({{ atelier['ID'] }});" style="cursor: pointer;background-color: #999;border-radius: 5px;">
            <strong>{{ atelier['Numero'] }} - {{ atelier['Nom'] }}</strong><br />
            {{ atelier['Description'] }}<br />
            Age: {{ atelier['Age mini'] }}  - {{ atelier['Age maxi'] }}<br />
            {{ atelier['Prix'] }}€
        </p>
        {% endfor %}
    """
    return render_template_string(template, ateliers=ateliers)


def listerHoraires():
    c = db.get_cursor()
    seances = db.callproc(c, 'listerSeances')
    template = """
        {% for seance in seances %}
        <p style="cursor: pointer;background-color: #777;border-radius: 5px;">
            <strong>{{ seance['Date'] }}</strong><br />
            {{ seance['Heure debut'] }} - {{ seance['Heure fin'] }}<br />
            Atelier {{ seance['Numero atelier'] }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def listerSeancesPourAtelier(atelierId):
    c = db.get_cursor()
    seances = db.callproc(c, 'listerSeancesPourAtelier', atelierId)
    template = """
        {% for seance in seances %}
        <p style="cursor: pointer;background-color: #777;border-radius: 5px;"
        onclick="ajouterAuPanier({{ seance['ID'] }});">
            <strong>{{ seance['Date'] }}</strong><br />
            {{ seance['Heure debut'] }} - {{ seance['Heure fin'] }}<br />
            Places restantes: {{ seance['Places Dispo'] }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def nouveauPanier():
    c = db.get_cursor()
    panier = db.callproc(c, 'obtenirIdPanier', '@idPanier')[0]['out_id']
    return str(panier)


def listerPanier(panierId):
    c = db.get_cursor()
    panier = db.callproc(c, 'afficherContenuPanier', panierId)
    template = """
        {% for seance in panier %}
        <p style="cursor: pointer;background-color: #444;border-radius: 5px;">
            <strong>{{ seance['Numero atelier'] }} - {{ seance['Nom atelier'] }}</strong><br />
            {{ seance['heureDebut'] }} - {{ seance['heurefin'] }}<br />
            {{ seance['prix'] }}<br />
            <button onclick="enleverDuPanier({{ seance['Id reservation'] }});">X</button>
        </p>
        {% endfor %}
    """
    return render_template_string(template, panier=panier)


def ajouterSeanceAuPanier(panierId, seanceId):
    c = db.get_cursor()
    result = db.callproc(c, 'ajouterSeanceAuPanier', panierId, seanceId, None, '@success')
    success = result[1][0]['out_result']
    return success


def enleverDuPanier(panierId, seanceId):
    c = db.get_cursor()
    result = db.callproc(c, 'enleverReservationDuPanier', panierId, seanceId, '@success')
    success = result[0]['out_result']
    return success
