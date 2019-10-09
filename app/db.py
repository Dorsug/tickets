import mysql.connector
from flask import g, current_app
from os import environ


# Setup so connection to db is done only once
def get_db():
    if 'db' not in g:
        config = current_app.config
        g.db = mysql.connector.connect(
            host=config['MYSQL_HOST'],
            database=config['MYSQL_DB'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            auth_plugin='mysql_native_password'
        )
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
