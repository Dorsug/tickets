from flask import render_template_string
from . import db


def listerAtelier():
    c = db.get_cursor()
    ateliers = db.Proc.listerAtelier(c)
    template = """
        {% for atelier in ateliers %}
        <p onclick="listerSeances(this, {{ atelier['id'] }});" class="bulle">
            <strong>{{ atelier['numero'] }} - {{ atelier['nom'] }}</strong><br />
            Age: {{ atelier['age_mini'] }}  - {{ atelier['age_maxi'] }}<br />
            {{ atelier['prix'] }}€
        </p>
        {% endfor %}
    """
    return render_template_string(template, ateliers=ateliers)


def listerHoraires():
    c = db.get_cursor()
    seances = db.callproc(c, "listerSeances")
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
    reservations = db.callproc(c, "listerPreReservations")
    template = """
        <input type="text" id="resaSearchBar" onkeyup="resaSearch()" placeholder="Recherche">
        {% for reservation in reservations %}
        <div class="bulle"
            onclick="showReservationContent({{ reservation.panier }}, this)">
            {{ reservation.nom }} {{ reservation.prenom }}<br />
            {{ reservation.mail }} <br />
            <form method="post" action="/impression" onsubmit="impression()">
                <input type="submit" value="Impression"></input>
                <input name="panierId" type="hidden" value="{{ reservation.panier }}">
            </form>
        </div>
        {% endfor %}
    """
    return render_template_string(template, reservations=reservations)


def listerSeancePourAtelier(atelierId, date):
    c = db.get_cursor()
    seances = db.Proc.listerSeancePourAtelier(c, atelierId, date)
    template = """
        {% for seance in seances %}
        <p 
            class="bulle{# if seance.placesRestantes <= 0 %} empty{% endif #}"
            onclick="ajouterAuPanier({{ seance['id'] }});"
        >
            <strong>{# {{ seance['Heure debut'] | time_split }} - {{ seance['Heure fin'] | time_split }} #}</strong><br />
            Places restantes: {# {{ seance['placesRestantes'] }} #}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def listerSeancesPourHoraire(horaire, date):
    c = db.get_cursor()
    seances = db.callproc(c, "listerSeancesPourHoraire", horaire, date)
    template = """
        {% for seance in seances %}
        <p class="bulle" onclick="ajouterAuPanier({{ seance['Id'] }});">
            <strong>{{ seance['AtelierNom'] }}</strong><br />
            <strong>{{ seance['Date'] }}</strong><br />
            {{ seance.heureDebut | time_split }} - {{ seance.heureFin | time_split }}<br />
            Places restantes: {{ seance.placesDispo }}
        </p>
        {% endfor %}
    """
    return render_template_string(template, seances=seances)


def listerPanier(panierId):
    c = db.get_cursor()
    panier = db.callproc(c, "afficherContenuPanier", panierId)
    template = """
        {% for seance in panier %}
        <p class="bulle">
            <strong>{{ seance['Numero atelier'] }} - {{ seance['Nom atelier'] }}</strong><br />
            {{ seance['heureDebut'] | time_split }} - {{ seance['heurefin'] | time_split }}<br />
            {{ seance['prix'] }}<br />
            <button onclick="enleverDuPanier({{ seance['seanceId'] }});">X</button>
        </p>
        {% endfor %}
    """
    return render_template_string(template, panier=panier)
