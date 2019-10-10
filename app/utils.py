from . import db
from hashlib import sha1
from os import mkdir
from PIL import Image, ImageDraw, ImageFont

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

from flask import current_app


def nouveauPanier():
    c = db.get_cursor()
    panier = db.callproc(c, 'obtenirIdPanier', '@idPanier')[0]['out_id']
    return str(panier)


def ajouterSeanceAuPanier(panierId, seanceId):
    c = db.get_cursor()
    result = db.callproc(c, 'ajouterSeanceAuPanier', panierId, seanceId, '@success')
    success = result[0]['out_result']
    return success


def enleverDuPanier(panierId, seanceId):
    c = db.get_cursor()
    result = db.callproc(c, 'enleverDuPanier', panierId, seanceId, '@success')
    success = result[0]['out_result']
    return success


def viderPanier(panierId):
    c = db.get_cursor()
    result = db.callproc(c, 'viderPanier', panierId, '@success')
    success = result[0]['out_result']
    return success


def marquePanierPaye(panierId):
    c = db.get_cursor()
    db.callproc(c, 'marquerPanierPaye', panierId, '@sucess')


def _clean_timedelta(td):
    # Enlève les secondes
    return ':'.join(str(td).split(':')[:2])


def _generationEtiquettes(numero, nom, date, debut, fin, structure):
    hash = sha1((f'{numero},{nom},{date},{debut},{fin}').encode('utf-8')).hexdigest()

    horaire = f"{_clean_timedelta(debut)} - {_clean_timedelta(fin)}"
    # Reverse dictionnary search
    date = next(key for key, value in current_app.config['DATES'].items() if value == str(date))

    # Création de de l'image
    img = Image.new(mode='L', size=(696, 291), color=255)
    font_normal = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 48)
    font_small = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 40)
    draw = ImageDraw.Draw(img)

    if len(nom) > 24:
        nom = nom[:24] + '\n' + nom[24:]

    # Ajout du texte
    draw.multiline_text((10, 10), f"N°{numero}. {nom}", fill=0, font=font_normal)
    draw.text((10, 170), f"{structure}", fill=0, font=font_small)
    draw.text((10, 230), horaire, fill=0, font=font_small)
    draw.text((500, 230), str(date), fill=0, font=font_small)

    filename = 'labels/' + hash + '.png'

    try:
        img.save(filename)
    except FileNotFoundError: # Si le repertoire 'labels' n'existe pas
        mkdir('labels')
        img.save(filename)
    return filename


def _sendToPrinter(images, imprimante_id):
    backend = 'linux_kernel'
    qlr = BrotherQLRaster('QL-800')

    instructions = convert(qlr=qlr, images=images, label='62red', red=True)
    send(
        instructions=instructions,
        printer_identifier=imprimante_id,
        backend_identifier=backend,
        blocking=False
    )


def impressionEtiquettes(panierId, imprimante):
    c = db.get_cursor()
    panier = db.callproc(c, 'afficherContenuPanier', panierId)
    images = []
    for seance in panier:
        images.append(
            _generationEtiquettes(
                numero=seance['Numero atelier'],
                nom=seance['Nom atelier'],
                date=seance['date'],
                debut=seance['heureDebut'],
                fin=seance['heurefin'],
                structure=seance['structure']
            )
        )
    imprimante_id = current_app.config['IMPRIMANTES'][int(imprimante) - 1]
    #_sendToPrinter(images, imprimante_id)
