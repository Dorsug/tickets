from . import app
from . import cli


def create_app():
    cli.register_cli(app.app)
    return app.app
