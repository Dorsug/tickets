from flask import Flask
import os.path
from os import mkdir
import math


def create_app():
    app = Flask("__tickets__", root_path=os.path.abspath("./tickets"))
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'tickets.sqlite'),
        LABELS=os.path.join(app.instance_path, 'labels'),
        NUMBER_OF_PRINTERS=4,
    )

    from tickets import utils
    app.jinja_env.globals.update(
        ceil=math.ceil,
        len=len,
        utils=utils,
        item_per_pages=app.config.get('item_per_pages', 10),
        config=app.config,
    )

    try:
        mkdir(app.instance_path)
    except FileExistsError:
        pass


    app.jinja_env.filters["ptime"] = utils.ptime

    from tickets import db
    app.teardown_appcontext(db.close_db)

    from tickets import cli
    cli.register_cli(app)

    from tickets import server
    app.register_blueprint(server.bp)

    app.add_url_rule("/", endpoint="index")

    return app
