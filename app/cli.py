from . import db
from . import utils


def register_cli(app):
    @app.cli.command("generate")
    def generate_labels():
        c = db.get_cursor()
        seances = db.callproc(c, "listerSeances")
        for seance in seances:
            print(seance)
            utils._generationEtiquettes(
                seance["numero"],
                seance["atelierNom"],
                seance["date"],
                seance["heureDebut"],
                seance["structureNom"],
            )
