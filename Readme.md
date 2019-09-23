# Gestickets2
## Répartition du code
`app.py`: Redistribution des requêtes

`db.py`: Gestion de la connexion à la base de données

`generate.py`: Création de html après lecture de la base de données.

`utils.py`: Modification de la base de données on fonction des requêtes reçus.

`assets/js/script.js`: Requêtes ajax

## Lancement
Environement nécessaire:
  - python3
  - `pip3 install flask mysql-connector`

Commande de lancement: `flask run`

Pour que l'interface soit accessible depuis un autre ordinateur: `flask run --host 0.0.0.0`

Pour lancer en mode développement: `FLASK_ENV=development flask run --host 0.0.0.0`

## Appels ajax
En règle général:
  - Si la requête récupère juste du contenue à afficher: `GET`
  - Si la requête modifie la base de données: `POST`
  - Si la requête supprime une entrée de la base de données: `DELETE`
