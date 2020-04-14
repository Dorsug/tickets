-- Liste les ateliers disponible
CREATE TABLE Atelier (
  id INTEGER PRIMARY KEY,    -- Clé primaire atelier
  -- structure INT NOT NULL,    -- Clé secondaire de la structure
  numero INT NOT NULL,       -- Numéro d’atelier
  nom VARCHAR(100) NOT NULL, -- Nom de l’atelier
  description TEXT,          -- Description de l’atelier
  age_mini INT NOT NULL,      -- Age minimum pour participer à l'atelier
  age_maxi INT NOT NULL,      -- Age maximum pour participer à l'atelier
  nombreplace INT NOT NULL,  -- Nombre de participants prévu'
  prix DECIMAL(6,2) NOT NULL -- Coût de l'aterlier
);

-- CREATE TABLE Structure (
--   pk_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Clé primaire Structure',
--   Nom varchar(255) NOT NULL COMMENT 'Nom de la structure',
--   Telephone varchar(10) COMMENT 'Numéro de téléphone',
--   Mail varchar(255) COMMENT 'Adresse mail de la structure',
--   Description text COMMENT 'Informations complémentaire lié à la structure'
-- ) COMMENT='Table listant les structures';
-- 
--
-- CREATE TABLE Client (
--   pk_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Clé primaire',
--   Nom varchar(16) NOT NULL COMMENT 'Nom de la personne',
--   Prenom varchar(16) NOT NULL COMMENT 'Prénom de la personne',
--   Mail varchar(255) NOT NULL COMMENT 'Adresse mailo de la personne'
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Identifier les clients ayant réservé une séance à l''avance';
-- 
-- 
-- CREATE TABLE MoyenPaiement (
--   pk_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Clé primaire moyen paiement',
--   Mode varchar(10) NOT NULL UNIQUE KEY COMMENT 'Mode du moyen de paiement'
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Liste des moyen de paiement';
-- 
-- 
-- CREATE TABLE CompteurPanier (
--   idPanier int(11) NOT NULL AUTO_INCREMENT UNIQUE KEY COMMENT 'Permet de déterminer un ID pour le panier',
--   Paye tinyint(1) NOT NULL COMMENT 'Spécifie si le panier à été payé ou non',
--   fk_moyPaiement int(11) DEFAULT NULL COMMENT 'Clé étrangère du moyen de paiement',
--   CodePostal char(5) COMMENT 'Code postal de la personne ayant payé',
--   fk_client int(11) DEFAULT NULL COMMENT 'Identifiant de la personne ayant réservée',
--   CONSTRAINT CompteurPanier_ibfk_1 FOREIGN KEY (fk_moyPaiement) REFERENCES MoyenPaiement (pk_id),
--   CONSTRAINT CompteurPanier_ibfk_2 FOREIGN KEY (fk_client) REFERENCES Client (pk_id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 
-- 
-- CREATE TABLE Seance (
--     pk_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Clé primaire',
--     date date NOT NULL COMMENT 'Date de la séance',
--     heureDebut time NOT NULL COMMENT 'Heure de début de la séance',
--     heureFin time NOT NULL COMMENT 'Heure de fin de la séance',
--     fk_atelier int(11) NOT NULL COMMENT 'Atelier concerné',
--     CONSTRAINT Seance_ibfk_1 FOREIGN KEY (fk_atelier) REFERENCES Atelier (pk_id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Séance dispensées par les ateliers';
-- 
-- 
-- CREATE TABLE Panier (
--   pk_id int(11) NOT NULL COMMENT 'Identifiant du panier',
--   fk_seance int(11) NOT NULL COMMENT 'ID de Séance résevée',
--   date date NOT NULL COMMENT 'Date de réservation',
--   heure time NOT NULL COMMENT 'Heure de réservatiuon',
--   CONSTRAINT Panier_ibfk_1 FOREIGN KEY (fk_seance) REFERENCES Seance (pk_id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Regroupe l''ensemble des reservations des séances';
