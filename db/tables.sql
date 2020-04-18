-- Liste les ateliers disponible
CREATE TABLE Atelier (
  id INTEGER PRIMARY KEY,    -- Clé primaire atelier
  structure INT NOT NULL,    -- Clé secondaire de la structure
  numero INT NOT NULL,       -- Numéro d’atelier
  nom VARCHAR(100) NOT NULL, -- Nom de l’atelier
  description TEXT,          -- Description de l’atelier
  age_mini INT NOT NULL,      -- Age minimum pour participer à l'atelier
  age_maxi INT NOT NULL,      -- Age maximum pour participer à l'atelier
  nombreplace INT NOT NULL,  -- Nombre de participants prévu'
  prix DECIMAL(6,2) NOT NULL, -- Coût de l'aterlier
  CONSTRAINT Atelier_fk_1 FOREIGN KEY (structure) REFERENCES Structure (id)
);

-- Séance dispensées par les ateliers
CREATE TABLE Seance (
  id INTEGER PRIMARY KEY,     -- Clé primaire
  datetime DATETIME NOT NULL, -- Date et Horaire de la séance
  atelier INT NOT NULL,       -- Atelier concerné
  CONSTRAINT Seance_fk_1 FOREIGN KEY (atelier) REFERENCES Atelier (id)
);

CREATE TABLE Structure (
  id INTEGER PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  telephone VARCHAR(10),
  email VARCHAR(255),
  description TEXT
);


CREATE TABLE Panier (
  id INTEGER PRIMARY KEY,
  paye tinyint(1) NOT NULL DEFAULT 0,
  moyenPaiement INTEGER,
  codePostal char(5)
);


CREATE TABLE ItemPanier (
  id INTEGER PRIMARY KEY,
  panier INTEGER NOT NULL,
  seance INTEGER NOT NULL,
  CONSTRAINT Panier_fk_1 FOREIGN KEY (panier) REFERENCES Panier (id)
  CONSTRAINT Panier_fk_2 FOREIGN KEY (seance) REFERENCES Seance (id)
);

-- CREATE TABLE Client (
--   pk_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Clé primaire',
--   Nom varchar(16) NOT NULL COMMENT 'Nom de la personne',
--   Prenom varchar(16) NOT NULL COMMENT 'Prénom de la personne',
--   Mail varchar(255) NOT NULL COMMENT 'Adresse mailo de la personne'
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Identifier les clients ayant réservé une séance à l''avance';
