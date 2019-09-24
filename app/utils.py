from . import db
from hashlib import sha1
from os import mkdir
from PIL import Image, ImageDraw, ImageFont


def nouveauPanier():
    c = db.get_cursor()
    panier = db.callproc(c, 'obtenirIdPanier', '@idPanier')[0]['out_id']
    return str(panier)


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


def marquePanierPaye(panierId):
    c = db.get_cursor()
    db.callproc(c, 'marquerPanierPaye', panierId, '@sucess')


def _clean_timedelta(td):
    # Enlève les secondes
    return ':'.join(str(td).split(':')[:2])


def generationEtiquettes(numero, nom, date, debut, fin):
    hash = sha1((f'{numero},{nom},{date},{debut},{fin}').encode('utf-8')).hexdigest()
    horaire = f"{_clean_timedelta(debut)} - {_clean_timedelta(fin)}"

    # Création de de l'image
    img = Image.new(mode='L', size=(696, 291), color=255)
    font_normal = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 60)
    font_small = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 40)
    draw = ImageDraw.Draw(img)

    # Ajout du texte
    draw.text((10, 10), f"{numero}. {nom}", fill=0, font=font_normal)
    draw.text((10, 170), horaire, fill=0, font=font_small)
    draw.text((10, 230), str(date), fill=0, font=font_small)

    try:
        img.save('labels/' + hash + '.png')
    except FileNotFoundError: # Si le repertoire 'labels' n'existe pas
        mkdir('labels')
    return hash


def impressionEtiquettes(panierId):
    c = db.get_cursor()
    panier = db.callproc(c, 'afficherContenuPanier', panierId)
    for seance in panier:
        hash = generationEtiquettes(
            numero=seance['Numero atelier'],
            nom=seance['Nom atelier'],
            date=seance['date'],
            debut=seance['heureDebut'],
            fin=seance['heurefin']
        )
