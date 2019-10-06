from flask import render_template_string
from . import db


def listerAtelier():
    c = db.get_cursor()
    ateliers = db.callproc(c, 'listerAtelier')
    template = """
        {% for atelier in ateliers %}
        <p onclick="listerSeances(this, {{ atelier['ID'] }});" class="bulle">
            <strong>{{ atelier['Numero'] }} - {{ atelier['Nom'] }}</strong><br />
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
        <p class="bulle">
            <strong>{{ seance['Date'] }}</strong><br />
            {{ seance['Heure debut'] }} - {{ seance['Heure fin'] }}<br />
            Atelier {{ seance['Numero atelier'] }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def listerReservations():
    c = db.get_cursor()
    reservations = db.callproc(c, 'listerPreReservations')
    template = """
        <input type="text" id="resaSearchBar" onkeyup="resaSearch()" placeholder="Recherche">
        {% for reservation in reservations %}
        <p class="bulle"
            onclick="Cookies.set('panierId', {{ reservation.panier }}); majInterfacePanier()">
            {{ reservation.nom }} {{ reservation.prenom }}<br />
            {{ reservation.mail }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, reservations=reservations)


def listerSeancesPourAtelier(atelierId, date):
    c = db.get_cursor()
    seances = db.callproc(c, 'listerSeancesPourAtelier', atelierId, date)
    template = """
        {% for seance in seances %}
        <p 
            class="bulle{% if seance.placesRestantes <= 0 %} empty{% endif %}"
            onclick="ajouterAuPanier({{ seance['ID'] }});"
        >
            <strong>{{ seance['Date'] }}</strong><br />
            {{ seance['Heure debut'] }} - {{ seance['Heure fin'] }}<br />
            Places restantes: {{ seance['placesRestantes'] }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def listerSeancesPourHoraire(horaire, date):
    c = db.get_cursor()
    seances = db.callproc(c, 'listerSeancesPourHoraire', horaire, date)
    template = """
        {% for seance in seances %}
        <p class="bulle" onclick="ajouterAuPanier({{ seance['Id'] }});">
            <strong>{{ seance['AtelierNom'] }}</strong><br />
            <strong>{{ seance['Date'] }}</strong><br />
            {{ seance['Heure debut'] }} - {{ seance['Heure fin'] }}<br />
            Places restantes: {{ seance['Places Dispo'] }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def listerPanier(panierId):
    c = db.get_cursor()
    panier = db.callproc(c, 'afficherContenuPanier', panierId)
    template = """
        {% for seance in panier %}
        <p class="bulle">
            <strong>{{ seance['Numero atelier'] }} - {{ seance['Nom atelier'] }}</strong><br />
            {{ seance['heureDebut'] }} - {{ seance['heurefin'] }}<br />
            {{ seance['prix'] }}<br />
            <button onclick="enleverDuPanier({{ seance['seanceId'] }});">X</button>
        </p>
        {% endfor %}
    """
    return render_template_string(template, panier=panier)
