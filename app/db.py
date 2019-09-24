import mysql.connector
from flask import g
from os import environ

mysql_config = {
    'user': environ.get('TICKETS_MYSQL_USER', 'root'),
    'password': environ.get('TICKETS_MYSQL_PASSWORD', 'roottoor'),
    'host': environ.get('TICKETS_MYSQL_HOST', '127.0.0.1')
}


# Setup so connection to db is done only once
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(database="gestickets2", auth_plugin='mysql_native_password', **mysql_config)
        g.db.autocommit = True
    return g.db


def get_cursor():
    cn = get_db()
    return cn.cursor()


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
    db = g.pop('db', None)
    if db is not None:
        db.close()
