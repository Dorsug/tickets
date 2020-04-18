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
