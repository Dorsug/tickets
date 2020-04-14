# Gestickets2
## Répartition du code
- `tickets`: Code python
    - `app.py`: Fichier principale, redistribution des requêtes
    - `db.py`: Gestion de la connexion à la base de données
    - `generate.py`: Création du html après lecture de la base de données.
    - `utils.py`: Modification de la base de données en fonction des requêtes reçues. / création des tickets
- `db`: Fichiers sql
- `assets/js/script.js`: Requêtes ajax

## Environement nécessaire:
  - python3
  - `pip3 install -r requirements.txt`

## Fichiers de configuration
`config.default` est réservé aux options communes à tout les environements.
Pour écraser localement des options, rajouter les au fichier `config.local`.
Notamment, l'option `MYSQL_PASSWORD` n'a pas de valeur par défaut.

## Lancement
Commande de lancement: `flask run`

Pour que l'interface soit accessible depuis un autre ordinateur: `flask run --host 0.0.0.0`

Pour lancer en mode développement: `FLASK_ENV=development flask run`

## Configuration

## Appels ajax
En règle général:
  - Si la requête récupère juste du contenu à afficher: `GET`
  - Si la requête modifie la base de données: `POST`
  - Si la requête supprime une entrée de la base de données: `DELETE`
