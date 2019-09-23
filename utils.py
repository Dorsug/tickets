import db


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
