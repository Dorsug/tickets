from . import db
from . import utils
import os
import sqlite3


def register_cli(app):
    @app.cli.command("generate")
    def generate_labels():
        c = db.get_cursor()
        seances = db.callproc(c, "listerSeances")
        for seance in seances:
            print(seance)
            utils._generationEtiquettes(
                numero=seance["numero"],
                nom=seance["atelierNom"],
                date=seance["date"],
                debut=seance["heureDebut"],
                structure=seance["structureNom"],
            )

    @app.cli.command("initdb")
    def initdb():
        print('-- initdb --')
        try:
            os.unlink(app.config['DATABASE'])
        except FileNotFoundError:
            pass
        db = sqlite3.connect(app.config['DATABASE'])
        with open('db/tables.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

    @app.cli.command("testdata")
    def testdata():
        print('-- testdata --')
        db = sqlite3.connect(app.config['DATABASE'])
        n = 20
        for i in range(int(n/2)):
            db.execute(f"INSERT INTO Structure (id, nom) VALUES ({i}, 'Structure {i}')")

        db.execute('''INSERT INTO Atelier VALUES
            (1,0,1,'Atelier 1',NULL,0,99,10,2,1),
            (2,1,2,'Atelier 2',NULL,0,99,10,2,2),
            (3,1,3,'Atelier 3',NULL,0,99,10,2,1),
            (4,2,4,'Atelier 4',NULL,0,99,10,2,3),
            (5,2,5,'Atelier 5',NULL,0,99,10,2,2),
            (6,3,6,'Atelier 6',NULL,0,99,10,2,4),
            (7,3,7,'Atelier 7',NULL,0,99,10,2,3),
            (8,4,8,'Atelier 8',NULL,0,99,10,2,1),
            (9,4,9,'Atelier 9',NULL,0,99,10,2,2),
            (10,5,10,'Atelier 10',NULL,0,99,10,2,4),
            (11,0,11,'Atelier 11',NULL,0,99,10,2,1),
            (12,1,12,'Atelier 12',NULL,0,99,10,2,2),
            (13,1,13,'Atelier 13',NULL,0,99,10,2,1),
            (14,2,14,'Atelier 14',NULL,0,99,10,2,3),
            (15,2,15,'Atelier 15',NULL,0,99,10,2,2),
            (16,3,16,'Atelier 16',NULL,0,99,10,2,4),
            (17,3,17,'Atelier 17',NULL,0,99,10,2,3),
            (18,4,18,'Atelier 18',NULL,0,99,10,2,1),
            (19,4,19,'Atelier 19',NULL,0,99,10,2,2),
            (20,5,20,'Atelier 20',NULL,0,99,10,2,4);''')

        db.execute('''UPDATE Atelier SET description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vulputate lacus nisl, eget sodales eros consectetur a. Aenean quis tincidunt urna. Integer a leo mauris. Donec in mi a mi scelerisque blandit non in lorem. Donec imperdiet tempor nulla in maximus. Quisque pellentesque nibh vitae dui maximus sollicitudin. Proin eget nulla in justo ornare accumsan. Donec at semper lorem, quis aliquam tellus. Pellentesque tincidunt ligula at elit suscipit tincidunt. Maecenas eleifend mauris vitae augue pellentesque elementum. Aenean tempus orci vitae arcu feugiat scelerisque.";''')

        db.execute('''INSERT INTO Pole VALUES
            (1, 'Pole 1', '0001b8'),
            (2, 'Pole 2', '62b82f'),
            (3, 'Pole 3', 'dad340'),
            (4, 'Pole 4', 'aa5bff'),
            (5, 'Pole 5', 'cd0b24');''')

        for i in range(1, n+1):
            # db.execute(f"""INSERT INTO
            #     Atelier (numero, nom, age_mini, age_maxi, nombreplace, prix, structure)
            #     VALUES ({i}, 'Atelier {i}', 0, 99, 10, 2.0, {floor(i/2)})"""
            # )
            for d in ['2019-10-19', '2019-10-20']:
                for t in ['10:30', '11:30', '14:00', '15:00', '16:00', '17:00', '18:00']:
                    db.execute(f"""INSERT INTO Seance (datetime, atelier)
                        VALUES ('{d} {t}', {i})"""
                    )
        db.commit()
        db.close()
