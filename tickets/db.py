import sqlite3
from flask import g, current_app
from os import environ


# Setup so connection to db is done only once
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def get_cursor(cur=None):
    if cur is None:
        return get_db().cursor()
    else:
        return cur


def select(req, *param, cur=None):
    cur = get_cursor(cur)
    return [dict(x) for x in cur.execute(req, *param).fetchall()]


class Proc(object):
    @staticmethod
    def listerAtelier(cursor):
        cursor.execute('''
            SELECT
                Atelier.id,
                Atelier.numero,
                Atelier.nom,
                Atelier.description,
                Atelier.age_mini,
                Atelier.age_maxi,
                Atelier.nombreplace,
                Atelier.prix
            FROM Atelier''')
        return cursor.fetchall()

    @staticmethod
    def listerSeancePourAtelier(cursor, atelierId, date):
        cursor.execute('''
            SELECT
                Seance.id AS "seance_id",
                Seance.datetime,
                Atelier.numero AS "atelier_numero",
                Atelier.nom AS "atelier_nom",
                Atelier.age_mini,
                Atelier.age_maxi,
                -- Atelier.nombreplace - (
                --     SELECT COUNT(Panier.fk_seance) FROM Panier
                --     WHERE Seance.pk_id = Panier.fk_seance
                -- ) AS placesRestantes,
                Atelier.nombrePlace,
                Atelier.prix
            FROM Seance
            INNER JOIN Atelier ON Seance.atelier = Atelier.id
            WHERE Seance.atelier = ?
            AND Seance.datetime >= ? AND Seance.datetime <= ?;''',
            (atelierId, date + ' 00:00:00', date + ' 23:59:59'))
        return cursor.fetchall()

    @staticmethod
    def nouveauPanier(cur=None):
        cur = get_cursor(cur)
        cur.execute('INSERT INTO Panier (id) VALUES (NULL)')
        cur.execute('SELECT last_insert_rowid() AS panierId')
        return cur.fetchone()['panierId']

    @staticmethod
    def ajouterSeanceAuPanier(panier, seance, cur=None):
        cur = get_cursor(cur)
        cur.execute('INSERT INTO ItemPanier (panier, seance) VALUES (?, ?)', (panier, seance))
        cur.execute('SELECT last_insert_rowid() AS itemId')
        return cur.fetchone()['itemId']

    @staticmethod
    def enleverDuPanier(itemId, cur=None):
        cur = get_cursor(cur)
        cur.execute('DELETE FROM ItemPanier WHERE id = ?', (itemId,))

    @staticmethod
    def viderPanier(panier, cur=None):
        cur = get_cursor(cur)
        cur.execute('DELETE FROM ItemPanier WHERE panier = ?', (panier,))

    @staticmethod
    def listerContenuPanier(panier, cur=None):
        cur = get_cursor(cur)
        return select('''
            SELECT
                ItemPanier.id,
                ItemPanier.seance,
                Seance.datetime,
                Atelier.nom AS atelier
            FROM ItemPanier
            JOIN Seance ON ItemPanier.seance = Seance.id
            JOIN Atelier ON Atelier.id = Seance.atelier
            WHERE panier = ?''',
            (panier,), cur=cur
        )

    @staticmethod
    def infoPanierPourEtiquettes(panier, cur=None):
        cur = get_cursor(cur)
        return select('''
            SELECT
                atelier.numero,
                atelier.nom AS atelierNom,
                seance.datetime,
                structure.nom AS structureNom
            FROM atelier
            INNER JOIN seance ON atelier.id = seance.atelier
            INNER JOIN itempanier ON seance.id = itempanier.seance
            INNER JOIN structure ON atelier.structure = structure.id
            WHERE itempanier.panier = ?''',
            (panier,), cur=cur
        )

    @staticmethod
    def payerPanier(panier, moyenPaiement, codePostal, cur=None):
        cur = get_cursor(cur)
        cur.execute('''
            UPDATE Panier
            SET
                Paye = 1,
                moyenPaiement = ?,
                CodePostal = ?
            WHERE id = ?''',
            (moyenPaiement, codePostal, panier)
        )

    @staticmethod
    def listerPlacesDispo(date, cur=None):
        cur = get_cursor(cur)
        return select('''
            SELECT
                time(Seance.datetime),
                Atelier.numero,
                Atelier.nom,
                Atelier.nombreplace - (
                    SELECT COUNT(itemPanier.seance) FROM itemPanier
                    WHERE Seance.id = itemPanier.seance
                ) AS placesRestantes
            FROM Seance
            INNER JOIN Atelier ON Seance.atelier = Atelier.id
            AND date(Seance.datetime) = ?''',
            (date,), cur=cur
        )

    @staticmethod
    def reserver(panier, nom, prenom, email, moyenPaiement, codePostal, cur=None):
        cur = get_cursor(cur)
        cur.execute('''
            UPDATE PANIER
            SET
                paye = 1,
                nom = ?,
                prenom = ?,
                email = ?,
                moyenPaiement = ?,
                codePostal = ?
            WHERE id = ?''',
            (nom, prenom, email, moyenPaiement, codePostal, panier)
        )

    @staticmethod
    def listerReservations(cur=None):
        cur = get_cursor(cur)
        clients = select('''SELECT id, nom, prenom, email, printed FROM panier WHERE nom IS NOT NULL ORDER BY id''', cur=cur)
        seances = {x['id']: list() for x in clients}
        items = select(f'''
            SELECT
                panier,
                atelier.nom,
                atelier.numero as ateliernumero,
                seance.datetime
            FROM itempanier
            JOIN seance ON itempanier.seance = seance.id
            JOIN atelier ON seance.atelier = atelier.id
            WHERE panier in ({','.join('?' for _ in seances.keys())})
            ORDER BY panier''',
            (*seances.keys(),), cur=cur
        )
        for item in items:
            seances[item['panier']].append(item)
        return clients, seances

    @staticmethod
    def markPrinted(panier):
        cur = get_cursor(None)
        cur.execute('''UPDATE panier SET printed = 1 WHERE id = ?''', (panier,))


def callproc(cursor, procname, *args):
    cursor.callproc(procname, args=args)

    results = []
    for subcursor in cursor.stored_results():
        columns = tuple([d[0] for d in subcursor.description])
        subresult = []
        for row in subcursor:
            subresult.append(dict(zip(columns, row)))
        results.append(subresult)
    if len(results) == 1:
        return results[0]
    else:
        return results


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.commit()
        db.close()
