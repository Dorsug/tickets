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
    data = c.execute('''
        SELECT DISTINCT(STRFTIME('%H:%M', datetime)) AS time
        FROM seance'''
    ).fetchall()
    return [x['time'] for x in data]

def get_possiblesDates():
    # /!\ if there is more than two distinct date in the db,
    # this is will spit out garbage
    c = db.get_cursor()
    data = c.execute('SELECT DISTINCT(DATE(datetime)) AS dates FROM seance').fetchall()
    return [x['dates'] for x in data]

def get_date(name):
    dates = get_possiblesDates()
    return dates[1] if name == 'Dimanche' else dates[0]

def get_time(datetime):
    return datetime.split(' ')[1]

def get_naturalDate(datetime):
    dates = get_possiblesDates()
    return 'Samedi' if datetime.split(' ')[0] == dates[0] else 'Dimanche'

def get_naturalDatetime(datetime):
    return get_naturalDate(datetime)[:3] + ' ' + get_time(datetime)

def payerPanier(panierId, modePaiement, codePostal):
    c = db.get_cursor()
    result = db.Proc.payerPanier(panierId, modePaiement, codePostal, c)

def marquePanierPaye(panierId):
    c = db.get_cursor()
    db.callproc(c, "marquerPanierPaye", panierId, "@sucess")


def reserver(*args):
    c = db.get_cursor()
    db.Proc.reserver(*args, c)


def _clean_timedelta(td):
    # Enlève les secondes
    return ":".join(str(td).split(":")[:2])


def sha1_cache(func):
    def wrapper(**k):
        strargs = f"{k['numero']},{k['nom']},{k['datetime']},{k['structure']}"
        hash = sha1(strargs.encode("utf-8")).hexdigest()
        filename = path.join(current_app.config.get('LABELS'), hash + ".png")
        if path.isfile(filename):
            return filename
        else:
            return func(**k, filename=filename)

    return wrapper


@sha1_cache
def _generationEtiquettes(numero, nom, datetime, structure, filename):
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
    draw.text((10, 230), get_naturalDatetime(datetime), fill=0, font=font_small)

    try:
        img.save(filename)
    except FileNotFoundError:  # Si le repertoire 'labels' n'existe pas
        mkdir(current_app.config.get('LABELS'))
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

IMPRIMANTES = [
    'file:///dev/usb/lp0',
    'file:///dev/usb/lp1',
    'file:///dev/usb/lp2',
    'file:///dev/usb/lp3'
]

def impressionEtiquettes(panierId, imprimante):
    c = db.get_cursor()
    panier = db.Proc.infoPanierPourEtiquettes(panierId, c)
    images = []
    for seance in panier:
        images.append(
            _generationEtiquettes(
                numero=seance["numero"],
                nom=seance["atelierNom"],
                datetime=seance["datetime"],
                structure=seance["structureNom"],
            )
        )
    imprimante_id = IMPRIMANTES[int(imprimante) - 1]
    t = threading.Thread(target=_sendToPrinter, args=(images, imprimante_id))
    t.start()


def ptime(time_info):
    """
    :param time_object time_info: "xx:xx:yy"
    :returns "xx:xx":
    """
    return str(time_info)[:5]
