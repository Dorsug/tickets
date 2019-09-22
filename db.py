import mysql.connector
from flask import g


# Setup so connection to db is done only once
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(user="root", password="roottoor", database="gestickets2", auth_plugin='mysql_native_password')
    return g.db


def get_cursor():
    cn = get_db()
    return cn.cursor()


def callproc(cursor, procname):
    cursor.callproc(procname)
    subcursor = list(cursor.stored_results())[0]

    columns = tuple([d[0] for d in subcursor.description])
    result = []
    for row in subcursor:
        result.append(dict(zip(columns, row)))
    return result


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
