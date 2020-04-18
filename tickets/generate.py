from flask import render_template_string
from . import db


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
