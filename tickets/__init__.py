from flask import Flask
import os.path
from os import mkdir


def create_app():
    app = Flask("__tickets__")
    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'tickets.sqlite'))

    try:
        mkdir(app.instance_path)
    except FileExistsError:
        pass


    from tickets import utils
    utils.load_jinja(app)

    from tickets import db
    app.teardown_appcontext(db.close_db)

    from tickets import cli
    cli.register_cli(app)

    from tickets import catalogue
    from tickets import admin
    app.register_blueprint(catalogue.bp)
    app.register_blueprint(admin.bp)

    return app
