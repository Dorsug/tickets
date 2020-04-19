from . import db
from hashlib import sha1
from os import mkdir, path
from PIL import Image, ImageDraw, ImageFont

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

from flask import current_app
import threading

from functools import lru_cache


@lru_cache
def get_horaires():
    c = db.get_cursor()
    data = c.execute('SELECT DISTINCT(TIME(datetime)) FROM seance').fetchall()
    return [x['(TIME(datetime))'] for x in data]


@lru_cache
def get_date(name):
    c = db.get_cursor()
    data = c.execute('SELECT DISTINCT(DATE(datetime)) FROM seance').fetchall()
    dates = [x['(DATE(datetime))'] for x in data]
    if name == 'dimanche':
        return dates[1]
    else:
        return dates[0]


def viderPanier(panierId):
    c = db.get_cursor()
    result = db.callproc(c, "viderPanier", panierId, "@success")
    success = result[0]["out_result"]
    return success


def payerPanier(panierId, modePaiement, codePostal):
    c = db.get_cursor()
    result = db.callproc(
        c,
        "payerPanier",
        panierId,
        modePaiement,
        (codePostal if codePostal else None),
        "@success",
    )
    success = result[0]["out_done"]
    return success


def marquePanierPaye(panierId):
    c = db.get_cursor()
    db.callproc(c, "marquerPanierPaye", panierId, "@sucess")


def _clean_timedelta(td):
    # Enlève les secondes
    return ":".join(str(td).split(":")[:2])


def sha1_cache(func):
    def wrapper(**k):
        strargs = f"{k['numero']},{k['nom']},{k['date']},{k['debut']},{k['structure']}"
        hash = sha1(strargs.encode("utf-8")).hexdigest()
        filename = "labels/" + hash + ".png"
        if path.isfile(filename):
            return filename
        else:
            return func(**k, filename=filename)

    return wrapper


@sha1_cache
def _generationEtiquettes(numero, nom, date, debut, structure, filename):
    # Reverse dictionnary search
    date = next(
        key for key, value in current_app.config["DATES"].items() if value == str(date)
    )

    # Création de de l'image
    img = Image.new(mode="L", size=(696, 291), color=255)
    font_normal = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 48)
    font_small = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 40)
    draw = ImageDraw.Draw(img)

    if len(nom) > 24:
        nom = nom[:24] + "\n" + nom[24:]

    # Ajout du texte
    draw.multiline_text((10, 10), f"N°{numero}. {nom}", fill=0, font=font_normal)
    draw.text((10, 170), f"{structure}", fill=0, font=font_small)
    draw.text((10, 230), f"{_clean_timedelta(debut)}", fill=0, font=font_small)
    draw.text((500, 230), str(date), fill=0, font=font_small)

    try:
        img.save(filename)
    except FileNotFoundError:  # Si le repertoire 'labels' n'existe pas
        mkdir("labels")
        img.save(filename)
    return filename


def _sendToPrinter(images, imprimante_id):
    backend = "linux_kernel"
    qlr = BrotherQLRaster("QL-800")

    instructions = convert(qlr=qlr, images=images, label="62red", red=True)
    send(
        instructions=instructions,
        printer_identifier=imprimante_id,
        backend_identifier=backend,
        blocking=False,
    )


def impressionEtiquettes(panierId, imprimante):
    c = db.get_cursor()
    panier = db.callproc(c, "afficherContenuPanier", panierId)
    images = []
    for seance in panier:
        images.append(
            _generationEtiquettes(
                numero=seance["Numero atelier"],
                nom=seance["Nom atelier"],
                date=seance["date"],
                debut=seance["heureDebut"],
                structure=seance["structure"],
            )
        )
    imprimante_id = current_app.config["IMPRIMANTES"][int(imprimante) - 1]
    t = threading.Thread(target=_sendToPrinter, args=(images, imprimante_id))
    t.start()
