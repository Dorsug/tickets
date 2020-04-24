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


    def time_split(timedelta):
        return ":".join(str(timedelta).split(":")[0:2])

    app.jinja_env.filters["time_split"] = time_split

    from tickets import db
    app.teardown_appcontext(db.close_db)

    from tickets import cli
    cli.register_cli(app)

    from tickets import server
    app.register_blueprint(server.bp)

    app.add_url_rule("/", endpoint="index")

    return app
