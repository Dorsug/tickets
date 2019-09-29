SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `gestickets2`
--

DELIMITER $$
--
-- Procédures
--


CREATE PROCEDURE listerSeancePourFiltres (
    IN in_idAtelier TEXT,
    IN in_debutApartirde TIME,
    IN in_agemini INT,
    IN in_agemaxi INT
)
BEGIN
    SET in_debutApartirde = IFNULL(in_debutApartirde, '00:00');
    SET in_agemini = IFNULL(in_agemini, 99);
    SET in_agemaxi = IFNULL(in_agemaxi, 0);

    SELECT
        Atelier.nom,
        Atelier.numero,
        Atelier.agemini,
        Atelier.agemaxi,
        Seance.heureDebut,
        Seance.heureFin
    FROM Seance
    INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
    WHERE FIND_IN_SET(Seance.fk_atelier, in_idAtelier) > 0
    AND Seance.heureDebut >= in_debutApartirde
    AND Atelier.agemini <= in_agemaxi
    AND Atelier.agemaxi >= in_agemini
    ORDER BY Atelier.numero, Seance.heureDebut;
END$$


CREATE DEFINER=`root`@`localhost` PROCEDURE `AfficherAssociation` (IN `in_idAssociation` INT(11))  SELECT * FROM Association
WHERE in_idAssociation = Association.pk_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AfficherAtelier` (IN `in_idAtelier` INT(11), OUT `out_nom` VARCHAR(16), OUT `out_description` TEXT, OUT `out_agemini` INT(11), OUT `out_agemaxi` INT(11), OUT `out_prix` INT(11), OUT `out_nombreplaces` INT(11), OUT `out_numero` INT(11))  NO SQL
    COMMENT 'Retourne les informations lié à l''atelier trouvé'
BEGIN
	SELECT COUNT(Atelier.pk_id) INTO @nbId FROM Atelier
	WHERE Atelier.pk_id = in_idAtelier;
    
    IF @nbId = 1 THEN
    	SELECT Atelier.numero, Atelier.nom,  Atelier.description, Atelier.agemini, Atelier.agemaxi, Atelier.prix, Atelier.nombreplace
        INTO out_numero, out_nom, out_description, out_agemini, out_agemaxi, out_prix, out_nombreplaces
        FROM Atelier WHERE Atelier.pk_id = in_idAtelier;
        
        SELECT out_numero, out_nom, out_description, out_agemini, out_agemaxi, out_prix, out_nombreplaces;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AfficherContenuPanier` (IN `in_idPanier` INT(11))  NO SQL
    COMMENT 'Retourne la liste des éléments contenus dans le panier'
SELECT Atelier.numero as 'Numero atelier', Atelier.nom as 'Nom atelier', Seance.date, Seance.heureDebut, Seance.heurefin, Atelier.prix, Reservation.pk_id as 'Id reservation', Client.pk_id as 'ID client', CompteurPanier.Paye as 'Est payé'
FROM Atelier
INNER JOIN Seance ON Atelier.pk_id = Seance.fk_atelier
INNER JOIN Reservation ON Reservation.fk_seance = Seance.pk_id
INNER JOIN Panier ON Reservation.pk_id = Panier.fk_reservation
INNER JOIN CompteurPanier ON CompteurPanier.idPanier = Panier.pk_id
LEFT JOIN Client ON Panier.fk_personne = Client.pk_id
WHERE Panier.pk_id = in_idPanier$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AfficherSeance` (IN `in_idSeance` INT(11), OUT `out_date` DATE, OUT `out_heuredebut` TIME, OUT `out_heurefin` TIME, OUT `out_numAtelier` INT(11), OUT `out_nomAtelier` VARCHAR(16), OUT `out_descAtelier` TEXT, OUT `out_ageminAtelier` INT(11), OUT `out_agemaxAtelier` INT(11), OUT `out_nbplace` INT(11))  NO SQL
    COMMENT 'Retourne les informations liées à la séance trouvée sinon rien'
BEGIN
	SELECT COUNT(Seance.pk_id) INTO @nbId FROM Seance
	WHERE Seance.pk_id = in_idSeance;
    
    IF @nbId = 1 THEN
    	SELECT Seance.date, Seance.heureDebut, Seance.heureFin, Atelier.numero, Atelier.nom, Atelier.description, Atelier.agemini, Atelier.agemaxi, Atelier.nombreplace
        INTO out_date, out_heuredebut, out_heurefin, out_numAtelier, out_nomAtelier, out_descAtelier, out_ageminAtelier, out_agemaxAtelier, out_nbplace
        FROM Seance, Atelier WHERE Seance.fk_atelier = Atelier.pk_id AND Seance.pk_id = in_idSeance;
        SELECT out_date, out_heuredebut, out_heurefin, out_numAtelier, out_nomAtelier, out_descAtelier, out_ageminAtelier, out_agemaxAtelier, out_nbplace;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AjouterClient` (IN `in_nom` VARCHAR(16), IN `in_prenom` VARCHAR(16), IN `in_mail` VARCHAR(255), OUT `out_id` INT)  NO SQL
    COMMENT 'Ajoute un nouveau client'
BEGIN
	SELECT COUNT(Client.Mail) INTO @nbMail FROM Client
	WHERE Client.Mail = in_mail;
    
    SET out_id = 0;
    IF @nbMail = 0 THEN
		IF in_nom <> '' THEN
			IF in_prenom <> '' THEN
				IF in_mail <> '' THEN
        			INSERT INTO `Client` (`pk_id`, `Nom`, `Prenom`, `Mail`) VALUES (NULL, in_nom, in_prenom, in_mail);
    				SET out_id = LAST_INSERT_ID();
				END IF;
			END IF;
    	END IF;
    END IF;
	SELECT out_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AjouterReservation` (IN `in_idseance` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Retourne l’ID de la reservation, 0 si échoué'
BEGIN
	SELECT COUNT(Seance.pk_id) INTO @nbID FROM Seance WHERE Seance.pk_id = in_idseance;

    SET out_result = 0;
    IF @nbID = 1 THEN
    	IF in_idseance <> '' THEN
        	SELECT CURRENT_DATE INTO @date;
            SELECT CURRENT_TIME INTO @heure;

        	INSERT INTO Reservation (Reservation.pk_id, Reservation.fk_seance, Reservation.date, Reservation.heure) VALUES (NULL, in_idseance, @date, @heure);
    		SET out_result = LAST_INSERT_ID();
    	END IF;
    END IF;
	SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AjouterSeanceAuPanier` (IN `in_idPanier` INT(11), IN `in_idSeance` INT(11), IN `in_idPersonne` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Retourne 1 si effectué 0 sinon'
BEGIN
	SET out_result = 0;
    CALL AjouterReservation (in_idSeance, @idReservation);

    IF @idReservation <> 0 THEN
		IF in_idPanier <> '' THEN
        	IF in_idPersonne = '' THEN
            	SET in_idPersonne = NULL;
            END IF;
            
        	INSERT INTO `Panier` (`pk_id`, `fk_reservation`, `fk_personne`) VALUES (in_idPanier, @idReservation, in_idPersonne);
    		SET out_result = 1;
        END IF;
    END IF;
    SELECT out_result;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `AjoutMoyenPaiement` (IN `in_MoyenPaiement` VARCHAR(10), OUT `out_done` BOOLEAN)  NO SQL
    COMMENT 'Permet d''ajouter un moyen de paiement'
BEGIN
	SET out_done = 0;
	SELECT COUNT(MoyenPaiement.pk_id) INTO @nbValPaiment FROM MoyenPaiement WHERE MoyenPaiement.Mode LIKE in_MoyenPaiement;
    
    IF @nbValPaiment = 0 THEN
    	INSERT INTO `MoyenPaiement` (`pk_id`, `Mode`) VALUES (NULL, in_MoyenPaiement);
    	SET out_done = 1;
    END IF;
    
    SELECT out_done;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ChercherClient` (IN `in_mail` VARCHAR(255))  SELECT 
    Client.pk_id AS "ID",
    Client.Nom AS "Nom",
    Client.Prenom AS "Prénom", 
    Client.Mail AS "Mail"
FROM Client
WHERE Client.Mail = in_mail$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CoutDuPanier` (IN `in_idPanier` INT(11))  SELECT SUM(Atelier.prix)
FROM Atelier
INNER JOIN Seance ON Atelier.pk_id = Seance.fk_atelier
INNER JOIN Reservation ON Reservation.fk_seance = Seance.pk_id
INNER JOIN Panier ON Reservation.pk_id = Panier.fk_reservation
LEFT JOIN Client ON Panier.fk_personne = Client.pk_id
WHERE Panier.pk_id = in_idPanier$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CreerAssociation` (OUT `out_id` INT, IN `in_nom` VARCHAR(255), IN `in_numero` VARCHAR(10), IN `in_mail` VARCHAR(255), IN `in_description` TEXT)  NO SQL
    COMMENT 'Retourne l''ID de l''association créée'
BEGIN
	SET out_id = 0;
    
    IF in_nom <> '' THEN
    	IF in_numero <> '' THEN
    		IF in_mail <> '' THEN
    			INSERT INTO `Association` (`pk_id`, `Nom`, `Telephone`, `Mail`, `Description`) VALUES (NULL, in_nom, in_numero, in_mail, in_description);
    			SET out_id = LAST_INSERT_ID();
    		END IF;
    	END IF;    
    END IF;

	SELECT out_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CreerAtelier` (IN `in_numero` INT(11) UNSIGNED, IN `in_nom` VARCHAR(16), IN `in_agemini` INT(11) UNSIGNED, IN `in_agemaxi` INT(11) UNSIGNED, IN `in_descripion` TEXT, IN `in_prix` DOUBLE(6,2), IN `in_nbplace` INT(11), OUT `out_id` INT)  NO SQL
    COMMENT 'Retourne l''ID de l''atelier créé'
BEGIN
	SELECT COUNT(Atelier.numero) INTO @nbNum FROM Atelier
	WHERE Atelier.numero = in_numero;
    
    SET out_id = 0;
    IF @nbNum = 0 THEN
    	IF in_numero <> '' THEN
			IF in_nom <> '' THEN
				IF in_agemini <> '' THEN
                    IF in_agemaxi <> '' THEN
						IF in_nbplace <> '' THEN
							IF in_prix <> '' THEN
    							IF in_agemini < in_agemaxi THEN
        							INSERT INTO `Atelier` (`pk_id`, `numero`, `nom`, `description`, `agemini`, `agemaxi`, `nombreplace`, `prix`) VALUES (NULL, in_numero, in_nom, in_descripion, in_agemini, in_agemaxi, in_nbplace, in_prix);
    								SET out_id = LAST_INSERT_ID();
								END IF;
							END IF;
						END IF;
					END IF;
				END IF;
			END IF;
    	END IF;
    END IF;
	SELECT out_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `CreerSeance` (IN `in_idatelier` INT(11), IN `in_date` DATE, IN `in_heuredebut` TIME, IN `in_heurefin` TIME, OUT `out_result` INT(11))  NO SQL
    COMMENT 'Retourne l''ID de la séance créée'
BEGIN
	SELECT COUNT(Seance.fk_atelier) INTO @nbID FROM Seance WHERE Seance.fk_atelier = in_idatelier AND Seance.date = in_date AND Seance.heureDebut = in_heuredebut AND Seance.heureFin = in_heurefin;
    
    SET out_result = 0;
    IF @nbID = 0 THEN
    	IF in_heuredebut < in_heurefin THEN
        	INSERT INTO Seance (Seance.pk_id, Seance.date, Seance.heureDebut, Seance.heureFin, Seance.fk_atelier) VALUES (NULL, in_date, in_heuredebut, in_heurefin, in_idatelier);
    		SET out_result = LAST_INSERT_ID();
    	END IF;
    END IF;
	SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `EnleverReservationDuPanier` (IN `in_idPanier` INT(11), IN `in_idReservation` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Supprime la réservation associée au panier'
BEGIN
	SET out_result = 0;
	SELECT COUNT(Reservation.pk_id) INTO @nbId FROM Panier, Reservation WHERE Panier.fk_reservation = Reservation.pk_id AND Panier.pk_id = in_idPanier AND Panier.fk_reservation = in_idReservation;
    
    IF @nbId = 1 THEN
    	SELECT COUNT(Reservation.pk_id) INTO @nbId FROM Reservation WHERE Reservation.pk_id = in_idReservation;
        IF @nbId = 1 THEN
        	DELETE FROM Panier WHERE Panier.pk_id = in_idPanier AND Panier.fk_reservation = in_idReservation;
            DELETE FROM Reservation WHERE Reservation.pk_id = in_idReservation;
    		SET out_result = 1;
        END IF;
	END IF;

    SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerAssociation` ()  SELECT
    Association.pk_id AS "ID",
    Association.Nom AS "Nom",
    Association.Telephone AS "Telephone",
    Association.Mail AS "Mail"
FROM Association$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerAtelier` ()  SELECT 
    Atelier.pk_id AS "ID",
    Atelier.numero AS "Numero",
    Atelier.nom AS "Nom", 
    Atelier.description AS "Description",
    Atelier.agemini AS "Age mini", 
    Atelier.agemaxi AS "Age maxi", 
    Atelier.nombreplace AS "Nombre de places",
    Atelier.prix AS "Prix"
FROM Atelier$$

CREATE DEFINER=`root`@`%` PROCEDURE `ListerAteliersPourHoraire` (IN `in_HeureDebut` TIME, IN `in_HeureFin` TIME)  NO SQL
    COMMENT 'Retourne la liste des atelier pour les créneaux horaires'
BEGIN
	IF in_HeureDebut <> '' THEN
    	IF in_HeureFin <> '' THEN
        	SELECT DISTINCT
            	Atelier.pk_id AS "ID",
			    Atelier.numero AS "Numero atelier", 
			    Atelier.nom AS "Nom de l'atelier", 
			    Atelier.description AS "Description de l'atelier", 
			    Atelier.agemini AS "Age mini", 
			    Atelier.agemaxi AS "Age maxi", 
			    Atelier.nombreplace AS "Nombre de places", 
			    Atelier.prix AS "Prix"
			FROM Seance, Atelier
			WHERE Seance.fk_atelier = Atelier.pk_id
			AND Seance.heureDebut >= in_HeureDebut
			AND Seance.heureFin <= in_HeureFin;
        END IF;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerClients` ()  SELECT 
    Client.pk_id AS "ID",
    Client.Nom AS "Nom",
    Client.Prenom AS "Prénom", 
    Client.Mail AS "Mail"
FROM Client$$

CREATE DEFINER=`root`@`%` PROCEDURE `ListerMoyensPaiement` ()  SELECT * FROM MoyenPaiement$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerReservations` ()  SELECT
	Reservation.pk_id AS "ID",
	Reservation.date AS "Date réservation",
    Reservation.heure AS "Heure réservation",
    Atelier.nom AS "Nom de l'atelier",
	Seance.date AS "Date de la séance", 
	Seance.heureDebut AS "Heure début", 
    Seance.heureFin AS "Heure fin", 
	Atelier.prix AS "Prix"
FROM Reservation, Seance, Atelier 
WHERE Reservation.fk_seance = Seance.pk_id
AND Seance.fk_atelier = Atelier.pk_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeances` ()  SELECT 
	Seance.pk_id AS "ID", 
    Seance.date AS "Date", 
    Seance.heureDebut AS "Heure debut", 
    Seance.heureFin AS "Heure fin", 
    Atelier.numero AS "Numero atelier", 
    Atelier.nom AS "Nom de l'atelier", 
    Atelier.description AS "Description de l'atelier", 
    Atelier.agemini AS "Age mini", 
    Atelier.agemaxi AS "Age maxi", 
    Atelier.nombreplace AS "Nombre de places", 
    Atelier.prix AS "Prix"
FROM Seance, Atelier 
WHERE Seance.fk_atelier = Atelier.pk_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesDispo` ()  NO SQL
    COMMENT 'Retourne la liste des reservations disponible'
SELECT *
FROM (SELECT 
	Seance.pk_id AS "ID", 
    Seance.date AS "Date", 
    Seance.heureDebut AS "Heure debut", 
    Seance.heureFin AS "Heure fin",
    Atelier.numero AS "Numero atelier", 
    Atelier.nom AS "Nom de l'atelier", 
    Atelier.description AS "Description de l'atelier", 
    Atelier.agemini AS "Age mini", 
    Atelier.agemaxi AS "Age maxi", 
    Atelier.nombreplace AS "Nb_Places",
    COUNT(Reservation.fk_seance) AS "Nb_Reserv",
    Atelier.prix AS "Prix"    
FROM Seance
INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance
GROUP BY Reservation.fk_seance) AS RESERVSEANCE
WHERE RESERVSEANCE.Nb_Places > RESERVSEANCE.Nb_Reserv$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesDispoPourAgeDate` (IN `in_date` DATE, IN `in_age` INT(11))  NO SQL
    COMMENT 'La liste des séances disponible pour un age à la date spécifiée'
BEGIN
	IF in_date <> '' THEN
		IF in_age <> '' THEN
            SELECT *
            FROM (SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin",
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age_mini", 
                Atelier.agemaxi AS "Age_maxi", 
                Atelier.nombreplace AS "Nb_Places",
                COUNT(Reservation.fk_seance) AS "Nb_Reserv",
                Atelier.prix AS "Prix"    
            FROM Seance
            INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
            INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance
            GROUP BY Reservation.fk_seance) AS RESERVSEANCE
            WHERE RESERVSEANCE.Nb_Places > RESERVSEANCE.Nb_Reserv
                AND RESERVSEANCE.date = in_date
                AND RESERVSEANCE.Age_mini <= in_age
                AND RESERVSEANCE.Age_maxi >= in_age;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesDispoPourAgeMaxiDate` (IN `in_date` DATE, IN `in_agemaxi` INT(11))  NO SQL
    COMMENT 'Liste les séances disponible pour un age maxi à la date donnée'
BEGIN
	IF in_date <> '' THEN
		IF in_agemaxi <> '' THEN
            SELECT *
            FROM (SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin",
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age_mini", 
                Atelier.agemaxi AS "Age_maxi", 
                Atelier.nombreplace AS "Nb_Places",
                COUNT(Reservation.fk_seance) AS "Nb_Reserv",
                Atelier.prix AS "Prix"    
            FROM Seance
            INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
            INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance
            GROUP BY Reservation.fk_seance) AS RESERVSEANCE
            WHERE RESERVSEANCE.Nb_Places > RESERVSEANCE.Nb_Reserv
                AND RESERVSEANCE.date = in_date
                AND RESERVSEANCE.Age_mini <= in_agemaxi;
		END IF;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesDispoPourAgeMiniDate` (IN `in_date` DATE, IN `in_agemini` INT(11))  NO SQL
    COMMENT 'Liste les séances disponible pour un age mini à la date donnée'
BEGIN
	IF in_date <> '' THEN
		IF in_agemini <> '' THEN
            SELECT *
            FROM (SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin",
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age_mini", 
                Atelier.agemaxi AS "Age_maxi", 
                Atelier.nombreplace AS "Nb_Places",
                COUNT(Reservation.fk_seance) AS "Nb_Reserv",
                Atelier.prix AS "Prix"    
            FROM Seance
            INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
            INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance
            GROUP BY Reservation.fk_seance) AS RESERVSEANCE
            WHERE RESERVSEANCE.Nb_Places > RESERVSEANCE.Nb_Reserv
                AND RESERVSEANCE.date = in_date
                AND RESERVSEANCE.Age_mini >= in_agemini;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesDispoPourAgeMiniMaxiDate` (IN `in_date` DATE, IN `in_agemini` INT(11), IN `in_agemaxi` INT(11))  NO SQL
    COMMENT 'Liste les séances disponible pour un age borné à la date donnée'
BEGIN
	IF in_date <> '' THEN
		IF in_agemini <> '' THEN
			IF in_agemaxi <> '' THEN
                SELECT *
                FROM (SELECT 
                    Seance.pk_id AS "ID", 
                    Seance.date AS "Date", 
                    Seance.heureDebut AS "Heure debut", 
                    Seance.heureFin AS "Heure fin",
                    Atelier.numero AS "Numero atelier", 
                    Atelier.nom AS "Nom de l'atelier", 
                    Atelier.description AS "Description de l'atelier", 
                    Atelier.agemini AS "Age_mini", 
                    Atelier.agemaxi AS "Age_maxi", 
                    Atelier.nombreplace AS "Nb_Places",
                    COUNT(Reservation.fk_seance) AS "Nb_Reserv",
                    Atelier.prix AS "Prix"    
                FROM Seance
                INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
                INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance
                GROUP BY Reservation.fk_seance) AS RESERVSEANCE
                WHERE RESERVSEANCE.Nb_Places > RESERVSEANCE.Nb_Reserv
                    AND RESERVSEANCE.date = in_date
                    AND RESERVSEANCE.Age_mini >= in_agemini
                    AND RESERVSEANCE.Age_maxi >= in_agemaxi;
            END IF;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesPourAgeDate` (IN `in_date` DATE, IN `in_age` INT(11))  NO SQL
    COMMENT 'Retourne la liste des séances pour un age à la date définie'
BEGIN
	IF in_date <> '' THEN
		IF in_age <> '' THEN
			SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin", 
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age mini", 
                Atelier.agemaxi AS "Age maxi", 
                Atelier.nombreplace AS "Nombre de places", 
                Atelier.prix AS "Prix"
            FROM Seance, Atelier 
            WHERE Seance.fk_atelier = Atelier.pk_id 
                AND Seance.date = in_date
                AND Atelier.agemini <= in_age
                AND Atelier.agemaxi >= in_age;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesPourAgeMaxiDate` (IN `in_date` DATE, IN `in_agemaxi` INT(11))  NO SQL
    COMMENT 'Retourne la liste des séances pour un age maxi à la date définie'
BEGIN
	IF in_date <> '' THEN
		IF in_agemini <> '' THEN
			SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin", 
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age mini", 
                Atelier.agemaxi AS "Age maxi", 
                Atelier.nombreplace AS "Nombre de places", 
                Atelier.prix AS "Prix"
            FROM Seance, Atelier 
            WHERE Seance.fk_atelier = Atelier.pk_id 
                AND Seance.date = in_date
                AND Atelier.agemaxi <= in_agemaxi;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesPourAgeMiniDate` (IN `in_date` DATE, IN `in_agemini` INT)  NO SQL
    COMMENT 'Retourne la liste des séances pour un age mini à la date définie'
BEGIN
	IF in_date <> '' THEN
		IF in_agemini <> '' THEN
			SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin", 
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age mini", 
                Atelier.agemaxi AS "Age maxi", 
                Atelier.nombreplace AS "Nombre de places", 
                Atelier.prix AS "Prix"
            FROM Seance, Atelier 
            WHERE Seance.fk_atelier = Atelier.pk_id 
                AND Seance.date = in_date
                AND Atelier.agemini >= in_agemini;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesPourAgeMinMaxDate` (IN `in_date` DATE, IN `in_agemini` INT(11), IN `in_agemaxi` INT(11))  NO SQL
    COMMENT 'Retourne les séances pour un age borné à la date définie'
BEGIN
	IF in_date <> '' THEN
		IF in_agemini <> '' THEN
			SELECT 
                Seance.pk_id AS "ID", 
                Seance.date AS "Date", 
                Seance.heureDebut AS "Heure debut", 
                Seance.heureFin AS "Heure fin", 
                Atelier.numero AS "Numero atelier", 
                Atelier.nom AS "Nom de l'atelier", 
                Atelier.description AS "Description de l'atelier", 
                Atelier.agemini AS "Age mini", 
                Atelier.agemaxi AS "Age maxi", 
                Atelier.nombreplace AS "Nombre de places", 
                Atelier.prix AS "Prix"
            FROM Seance, Atelier 
            WHERE Seance.fk_atelier = Atelier.pk_id 
                AND Seance.date = in_date
                AND Atelier.agemini >= in_agemini
                AND Atelier.agemaxi <= in_agemaxi;
		END IF;
	END IF;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `ListerSeancesPourAtelier` (IN `in_idAtelier` INT(11))  NO SQL
    COMMENT 'Retourne la liste des séances pour un atelier'
BEGIN
	IF in_idAtelier <> '' THEN
		SELECT 
			Seance.pk_id AS "ID", 
		    Seance.date AS "Date", 
		    Seance.heureDebut AS "Heure debut", 
		    Seance.heureFin AS "Heure fin",
		    Atelier.numero AS "Numero atelier", 
		    Atelier.nom AS "Nom de l'atelier", 
		    Atelier.description AS "Description de l'atelier", 
		    Atelier.agemini AS "Age mini", 
		    Atelier.agemaxi AS "Age maxi",
            Atelier.nombreplace-COUNT(Reservation.fk_seance) AS "Places Dispo",
			Atelier.prix AS "Prix"    
		FROM Seance
		INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
		INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance
		WHERE Seance.fk_atelier = in_idAtelier
		GROUP BY Reservation.fk_seance;
	END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ListerSeancesPourDate` (IN `in_date` DATE)  SELECT 
	Seance.pk_id AS "ID", 
    Seance.date AS "Date", 
    Seance.heureDebut AS "Heure debut", 
    Seance.heureFin AS "Heure fin", 
    Atelier.numero AS "Numero atelier", 
    Atelier.nom AS "Nom de l'atelier", 
    Atelier.description AS "Description de l'atelier", 
    Atelier.agemini AS "Age mini", 
    Atelier.agemaxi AS "Age maxi", 
    Atelier.nombreplace AS "Nombre de places", 
    Atelier.prix AS "Prix"
FROM Seance, Atelier
WHERE Seance.fk_atelier = Atelier.pk_id AND Seance.date = in_date$$

CREATE DEFINER=`root`@`%` PROCEDURE `ListerSeancesPourHoraire` (IN `in_HeureDebut` TIME, IN `in_HeureFin` TIME)  NO SQL
    COMMENT 'Retourne la liste des Séances pour les créneaux horaires'
BEGIN
	IF in_HeureDebut <> '' THEN
    	IF in_HeureFin <> '' THEN
        	SELECT 
				Seance.pk_id AS "ID Seance", 
				Seance.date AS "Date", 
				Seance.heureDebut AS "Heure debut", 
				Seance.heureFin AS "Heure fin", 
				Atelier.numero AS "Numero atelier", 
				Atelier.nom AS "Nom de l'atelier", 
				Atelier.description AS "Description de l'atelier", 
				Atelier.agemini AS "Age mini", 
				Atelier.agemaxi AS "Age maxi", 
				Atelier.nombreplace AS "Nombre de places", 
				Atelier.prix AS "Prix"
			FROM Seance, Atelier
			WHERE Seance.fk_atelier = Atelier.pk_id
			AND Seance.heureDebut >= in_HeureDebut
			AND Seance.heureFin <= in_HeureFin;
        END IF;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `MarquerPanierNONPaye` (IN `in_idPanier` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Permet de définir qu''un panier n''a pas été payé'
BEGIN
	SET out_result = 0;
	
	SELECT COUNT(CompteurPanier.idPanier) INTO @nbPanier FROM CompteurPanier
	WHERE CompteurPanier.idPanier = in_idPanier;	
	
	IF @nbPanier = 1 THEN
		UPDATE CompteurPanier 
        	SET CompteurPanier.Paye = '0',
            CompteurPanier.fk_moyPaiement = NULL,
            CompteurPanier.CodePostal = '00000'
            WHERE CompteurPanier.idPanier = in_idPanier;
		SET out_result = 1;
	END IF;
	
	SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `MarquerPanierPaye` (IN `in_idPanier` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Permet de définir qu''un panier a été payé'
BEGIN
	SET out_result = 0;
	
	SELECT COUNT(CompteurPanier.idPanier) INTO @nbPanier FROM CompteurPanier
	WHERE CompteurPanier.idPanier = in_idPanier;	
	
	IF @nbPanier = 1 THEN
		UPDATE CompteurPanier SET Paye = '1' WHERE CompteurPanier.idPanier = in_idPanier;
		SET out_result = 1;
	END IF;
	
	SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ModifierAssociation` (IN `in_idassociation` INT(11), OUT `out_result` INT, IN `in_nom` VARCHAR(255), IN `in_numero` INT(10), IN `in_mail` VARCHAR(255), IN `in_description` TEXT)  NO SQL
    COMMENT 'Retourne 1 si effectué 0 sinon'
BEGIN
	SELECT COUNT(Association.pk_id) INTO @idAsso FROM Association
	WHERE Association.pk_id = in_idassociation;
    
    SET out_result = 0;
    IF @idAsso = 1 THEN
    	IF in_nom <> '' THEN
			IF in_numero <> '' THEN
				IF in_mail <> '' THEN
    				UPDATE Association SET Association.Nom = in_nom, Association.Telephone = in_numero, Association.Mail = in_mail, Association.Description = in_description WHERE Association.pk_id = in_idassociation; 
    				SET out_result = 1;
				END IF;
			END IF;
		END IF;
   END IF;
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ModifierAtelier` (IN `in_idatelier` INT(11), IN `in_numero` INT(11), IN `in_nom` VARCHAR(16), IN `in_description` TEXT, IN `in_agemini` INT(11), IN `in_agemaxi` INT(11), IN `in_nbplace` INT(11), IN `in_prix` DECIMAL(6,2), OUT `out_result` INT)  NO SQL
    COMMENT 'Retourne 1 si effectué 0 sinon'
BEGIN
	SELECT COUNT(Atelier.pk_id) INTO @idAtel FROM Atelier
	WHERE Atelier.pk_id = in_idatelier;
    
    SET out_result = 0;
    IF @idAtel = 1 THEN
    	IF in_numero <> '' THEN
			IF in_nom <> '' THEN
				IF in_description <> '' THEN
					IF in_agemini <> '' THEN
                    	IF in_agemaxi <> '' THEN
							IF in_nbplace <> '' THEN
								IF in_prix <> '' THEN
    								UPDATE Atelier SET Atelier.numero = in_numero, Atelier.nom = in_nom, Atelier.description = in_description, Atelier.agemini = in_agemini, Atelier.agemaxi = in_agemaxi, Atelier.nombreplace = in_nbplace, Atelier.prix = in_prix WHERE Atelier.pk_id = in_idatelier; 
    								SET out_result = 1;
								END IF;
							END IF;
						END IF;
					END IF;
				END IF;
			END IF;
		END IF;
   END IF;
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ModifierClient` (IN `in_nom` VARCHAR(16), IN `in_prenom` VARCHAR(16), IN `in_mail` VARCHAR(255), IN `in_idclient` INT, OUT `out_id` INT)  NO SQL
    COMMENT 'Retourne 1 si effectué 0 sinon'
BEGIN
	SELECT COUNT(Client.Mail) INTO @in_idclient FROM Client
	WHERE Client.pk_id = in_idclient;
    
    SET out_id = 0;
    IF @in_idclient = 1 THEN
		IF in_nom <> '' THEN
			IF in_prenom <> '' THEN
				IF in_mail <> '' THEN
					UPDATE Client SET Client.Nom = in_nom, Client.Prenom = in_prenom, Client.Mail = in_mail
					WHERE Client.pk_id = in_idclient;
                    SET out_id = 1;
				END IF;
			END IF;
    	END IF;
    END IF;
	SELECT out_id;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `ModifierMoyenPaiement` (IN `id_MoyenPaiement` INT(11), IN `in_MoyenModifie` VARCHAR(10), OUT `out_done` BOOLEAN)  NO SQL
    COMMENT 'Permet de modifier le moyen de paiement'
BEGIN
	SET out_done = 0;
    
    SELECT COUNT(MoyenPaiement.pk_id) INTO @nbID 
    FROM MoyenPaiement 
    WHERE MoyenPaiement.pk_id = id_MoyenPaiement;
    
    IF @nbID = 1 THEN
		UPDATE `MoyenPaiement` SET `Mode` = in_MoyenModifie WHERE `MoyenPaiement`.`pk_id` = id_MoyenPaiement;
    	SET out_done = 1;
    END IF;
    
    SELECT out_done;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ModifierSeance` (IN `in_idseance` INT(11), OUT `out_result` INT(11), IN `in_date` DATE, IN `in_heuredebut` TIME, IN `in_heurefin` TIME, IN `in_idatelier` INT(11))  NO SQL
    COMMENT 'Retourne 1 si effectué avec succès, 0 sinon'
BEGIN
	SELECT COUNT(Seance.pk_id) INTO @nbID FROM Seance WHERE Seance.pk_ID = in_idseance;
    
	SET out_result = 0;
    IF @nbID = 1 THEN
		IF in_date <> '' THEN
			IF in_heuredebut <> '' THEN
				IF in_heurefin <> '' THEN
					IF in_idseance <> '' THEN
						UPDATE Seance SET Seance.date = in_date, Seance.heureDebut = in_heuredebut, Seance.heureFin = in_heurefin, Seance.fk_atelier = in_idatelier WHERE Seance.pk_id = in_idseance;
						SET out_result = 1;
					END IF;
				END IF;
			END IF;
		END IF;
	END IF;
	SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenirIDpanier` (OUT `out_id` INT(11))  NO SQL
    COMMENT 'Crée une entrée et retourne le dernier ID de la table'
BEGIN
	INSERT INTO CompteurPanier (CompteurPanier.idPanier) VALUES (NULL);
    SET out_id = LAST_INSERT_ID();

	SELECT out_id;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `PayerPanier` (IN `in_idPanier` INT(11), IN `in_idMoyPaie` INT(11), IN `in_CodPost` VARCHAR(5), OUT `out_done` BOOLEAN)  NO SQL
    COMMENT 'Paie le panier en indiquant moyen de paiement et code postal'
BEGIN
	SET out_done = 0;
	
	SELECT COUNT(CompteurPanier.idPanier) INTO @nbPanier FROM CompteurPanier
	WHERE CompteurPanier.idPanier = in_idPanier;	
    
	IF @nbPanier = 1 THEN
    	SELECT COUNT(MoyenPaiement.pk_id) INTO @nbID 
        	FROM MoyenPaiement
        	WHERE MoyenPaiement.pk_id = in_idMoyPaie;
        IF @nbID = 1 THEN
			UPDATE CompteurPanier 
            	SET CompteurPanier.Paye = '1', 
            	CompteurPanier.fk_moyPaiement = in_idMoyPaie,
                CompteurPanier.CodePostal = in_CodPost
            	WHERE CompteurPanier.idPanier = in_idPanier;
			SET out_done = 1;
    	END IF;
	END IF;
	
	SELECT out_done;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SupprimerAssociation` (IN `in_idAssociation` INT(11), OUT `out_result` INT)  NO SQL
    COMMENT 'Retourne 1 si effectué, 0 sinon'
BEGIN
	SELECT COUNT(Association.pk_id) INTO @nbId FROM Association
	WHERE Association.pk_id = in_idAssociation;
    
    IF @nbId = 1 THEN
    	DELETE FROM Association WHERE Association.pk_id = in_idAssociation;
    	SET out_result = 1;
    ELSE
    	SET out_result = 0;
       END IF;
   
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SupprimerAtelier` (IN `in_idAtelier` INT, OUT `out_result` INT)  NO SQL
    COMMENT 'Retourne 1 si effectué, 0 sinon'
BEGIN
	SELECT COUNT(Atelier.pk_id) INTO @nbId FROM Atelier
	WHERE Atelier.pk_id = in_idAtelier;
    
    IF @nbId = 1 THEN
    	DELETE FROM Atelier WHERE Atelier.pk_id = in_idAtelier;
    	SET out_result = 1;
    ELSE
    	SET out_result = 0;
       END IF;
   
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SupprimerClient` (IN `in_idClient` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Retourne 1 si effectué, 0 sinon'
BEGIN
	SELECT COUNT(Client.pk_id) INTO @nbId FROM Client
	WHERE Client.pk_id = in_idClient;
    
    IF @nbId = 1 THEN
    	DELETE FROM Client WHERE Client.pk_id = in_idClient;
    	SET out_result = 1;
    ELSE
    	SET out_result = 0;
       END IF;
   
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `SupprimerMoyenPaiement` (IN `id_MoyenPaiement` INT(11), OUT `out_done` BOOLEAN)  NO SQL
    COMMENT 'Supprime un moyen de paiement'
BEGIN
	SET out_done = 0;
    
    SELECT COUNT(MoyenPaiement.pk_id) INTO @nbID 
    	FROM MoyenPaiement 
    	WHERE MoyenPaiement.pk_id = id_MoyenPaiement;
    
    IF @nbID = 1 THEN
        DELETE FROM `MoyenPaiement` 
        	WHERE `MoyenPaiement`.`pk_id` = id_MoyenPaiement;
    	SET out_done = 1;
    END IF;
    
    SELECT out_done;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SupprimerReservation` (IN `in_idreservation` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Retourne 1 si effectué, 0 sinon'
BEGIN
	SELECT COUNT(Reservation.pk_id) INTO @nbId FROM Reservation
	WHERE Reservation.pk_id = in_idreservation;
    
    SET out_result = 0;
    
    IF @nbId = 1 THEN
    	DELETE FROM Reservation WHERE Reservation.pk_id = in_idreservation;
    	SET out_result = 1;
	END IF;
   
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SupprimerSeance` (IN `in_idseance` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Retourne 1 si effectué, 0 sinon'
BEGIN
	SELECT COUNT(Seance.pk_id) INTO @nbId FROM Seance
	WHERE Seance.pk_id = in_idseance;
    
    IF @nbId = 1 THEN
    	DELETE FROM Seance WHERE Seance.pk_id = in_idseance;
    	SET out_result = 1;
    ELSE
    	SET out_result = 0;
       END IF;
   
   SELECT out_result;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `ViderPanier` (IN `in_idPaner` INT(11), OUT `out_result` INT(11))  NO SQL
    COMMENT 'Enlève toute les séances du panier'
BEGIN
	SET out_result = 0;
	SELECT COUNT(Reservation.pk_id) INTO @nbReserv FROM Panier, Reservation WHERE Panier.fk_reservation = Reservation.pk_id AND Panier.pk_id = 1;
    
    WHILE @nbReserv > 0 DO
    SELECT Panier.fk_reservation INTO @idReserv FROM Panier WHERE Panier.pk_id = 1 LIMIT 1;
    DELETE FROM Panier WHERE Panier.pk_id = in_idPaner AND Panier.fk_reservation = @idReserv;
    DELETE FROM Reservation WHERE Reservation.pk_id = @idReserv;
    
    SELECT COUNT(Reservation.pk_id) INTO @nbReserv FROM Panier, Reservation WHERE Panier.fk_reservation = Reservation.pk_id AND Panier.pk_id = in_idPaner;
    END WHILE;
	SET out_result = 1;
    SELECT out_result;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `Association`
--

CREATE TABLE `Association` (
  `pk_id` int(11) NOT NULL COMMENT 'Clé primaire association',
  `Nom` varchar(255) NOT NULL COMMENT 'Nom de l''association',
  `Telephone` varchar(10) COMMENT 'Numéro de téléphone',
  `Mail` varchar(255) COMMENT 'Adresse mail de l''association',
  `Description` text COMMENT 'Informations complémentaire lié à l''association'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Table listant les associations';

-- --------------------------------------------------------

--
-- Structure de la table `Atelier`
--

CREATE TABLE `Atelier` (
  `pk_id` int(11) NOT NULL COMMENT 'Clé primaire atelier',
  `fk_association` int(11) NOT NULL COMMENT 'Clé secondaire de l''association ',
  `numero` int(11) NOT NULL COMMENT 'Numéro d’atelier',
  `nom` varchar(100) NOT NULL COMMENT 'Nom de l’atelier',
  `description` text NOT NULL COMMENT 'Description de l’atelier',
  `agemini` int(11) NOT NULL COMMENT 'Age minimum pour participer à l’atelier',
  `agemaxi` int(11) NOT NULL COMMENT 'Age maximum pour participer à l’atelier',
  `nombreplace` int(11) NOT NULL COMMENT 'Nombre de participants prévu',
  `prix` decimal(6,2) NOT NULL COMMENT 'Coût de l''aterlier'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Liste les ateliers disponible';

-- --------------------------------------------------------

--
-- Structure de la table `Client`
--

CREATE TABLE `Client` (
  `pk_id` int(11) NOT NULL COMMENT 'Clé primaire',
  `Nom` varchar(16) NOT NULL COMMENT 'Nom de la personne',
  `Prenom` varchar(16) NOT NULL COMMENT 'Prénom de la personne',
  `Mail` varchar(255) NOT NULL COMMENT 'Adresse mailo de la personne'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Identifier les clients ayant réservé une séance à l''avance';

-- --------------------------------------------------------

--
-- Structure de la table `CompteurPanier`
--

CREATE TABLE `CompteurPanier` (
  `idPanier` int(11) NOT NULL COMMENT 'Permet de déterminer un ID pour le panier',
  `Paye` tinyint(1) NOT NULL COMMENT 'Spécifie si le panier à été payé ou non',
  `fk_moyPaiement` int(11) DEFAULT NULL COMMENT 'Clé étrangère du moyen de paiement',
  `CodePostal` char(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '00000' COMMENT 'Code postail de la personne ayant payé'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `MoyenPaiement`
--

CREATE TABLE `MoyenPaiement` (
  `pk_id` int(11) NOT NULL COMMENT 'Clé primaire moyen paiement',
  `Mode` varchar(10) NOT NULL COMMENT 'Mode du moyen de paiement'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Liste des moyen de paiement';

-- --------------------------------------------------------

--
-- Structure de la table `Panier`
--

CREATE TABLE `Panier` (
  `pk_id` int(11) NOT NULL COMMENT 'Identifiant du panier',
  `fk_reservation` int(11) NOT NULL COMMENT 'Identifie la réservation concernée',
  `fk_personne` int(11) DEFAULT NULL COMMENT 'Identifiant de la personne ayant réservée'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Etablit la relation entre les réservations et les personnes';

-- --------------------------------------------------------

--
-- Structure de la table `Reservation`
--

CREATE TABLE `Reservation` (
  `pk_id` int(11) NOT NULL COMMENT 'Clé primaire reservation',
  `fk_seance` int(11) NOT NULL COMMENT 'ID de Séance résevée',
  `date` date NOT NULL COMMENT 'Date de réservation',
  `heure` time NOT NULL COMMENT 'Heure de réservatiuon'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Regroupe l''ensemble des reservations des séances';

--
-- Déclencheurs `Reservation`
--
DELIMITER $$
CREATE TRIGGER `VerifReservation` AFTER INSERT ON `Reservation` FOR EACH ROW BEGIN
	SELECT 
    Atelier.nombreplace - COUNT(Reservation.fk_seance) AS "Dispo" INTO @dispo
	FROM Seance
	INNER JOIN Atelier ON Seance.fk_atelier = Atelier.pk_id
	INNER JOIN Reservation ON Seance.pk_id = Reservation.fk_seance AND Seance.pk_id = NEW.fk_seance
	GROUP BY Reservation.fk_seance;
    
    IF @dispo < 0 THEN
    	DELETE FROM Reservation WHERE Reservation.pk_id = NEW.pk_id;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `Seance`
--

CREATE TABLE `Seance` (
  `pk_id` int(11) NOT NULL COMMENT 'Clé primaire',
  `date` date NOT NULL COMMENT 'Date de la séance',
  `heureDebut` time NOT NULL COMMENT 'Heure de début de la séance',
  `heureFin` time NOT NULL COMMENT 'Heure de fin de la séance',
  `fk_atelier` int(11) NOT NULL COMMENT 'Atelier concerné'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Séance dispensées par les ateliers';

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Association`
--
ALTER TABLE `Association`
  ADD PRIMARY KEY (`pk_id`);

--
-- Index pour la table `Atelier`
--
ALTER TABLE `Atelier`
  ADD PRIMARY KEY (`pk_id`),
  ADD KEY `fk_association` (`fk_association`);

--
-- Index pour la table `Client`
--
ALTER TABLE `Client`
  ADD UNIQUE KEY `pk_id` (`pk_id`);

--
-- Index pour la table `CompteurPanier`
--
ALTER TABLE `CompteurPanier`
  ADD UNIQUE KEY `idPaier` (`idPanier`),
  ADD KEY `fk_moyPaiement` (`fk_moyPaiement`);

--
-- Index pour la table `MoyenPaiement`
--
ALTER TABLE `MoyenPaiement`
  ADD PRIMARY KEY (`pk_id`),
  ADD UNIQUE KEY `Mode` (`Mode`);

--
-- Index pour la table `Panier`
--
ALTER TABLE `Panier`
  ADD KEY `fk_personne` (`fk_personne`),
  ADD KEY `pk_id` (`pk_id`),
  ADD KEY `fk_reservation` (`fk_reservation`);

--
-- Index pour la table `Reservation`
--
ALTER TABLE `Reservation`
  ADD PRIMARY KEY (`pk_id`),
  ADD KEY `fk_seance` (`fk_seance`),
  ADD KEY `fk_seance_2` (`fk_seance`);

--
-- Index pour la table `Seance`
--
ALTER TABLE `Seance`
  ADD PRIMARY KEY (`pk_id`),
  ADD KEY `fk_atelier` (`fk_atelier`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Association`
--
ALTER TABLE `Association`
  MODIFY `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire association';

--
-- AUTO_INCREMENT pour la table `Atelier`
--
ALTER TABLE `Atelier`
  MODIFY `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire atelier';

--
-- AUTO_INCREMENT pour la table `Client`
--
ALTER TABLE `Client`
  MODIFY `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire';

--
-- AUTO_INCREMENT pour la table `CompteurPanier`
--
ALTER TABLE `CompteurPanier`
  MODIFY `idPanier` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Permet de déterminer un ID pour le panier';

--
-- AUTO_INCREMENT pour la table `MoyenPaiement`
--
ALTER TABLE `MoyenPaiement`
  MODIFY `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire moyen paiement';

--
-- AUTO_INCREMENT pour la table `Reservation`
--
ALTER TABLE `Reservation`
  MODIFY `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire reservation';

--
-- AUTO_INCREMENT pour la table `Seance`
--
ALTER TABLE `Seance`
  MODIFY `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Clé primaire';

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `CompteurPanier`
--
ALTER TABLE `CompteurPanier`
  ADD CONSTRAINT `LstMoyPaiement` FOREIGN KEY (`fk_moyPaiement`) REFERENCES `MoyenPaiement` (`pk_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `Panier`
--
ALTER TABLE `Panier`
  ADD CONSTRAINT `Panier_ibfk_1` FOREIGN KEY (`fk_personne`) REFERENCES `Client` (`pk_id`),
  ADD CONSTRAINT `Panier_ibfk_2` FOREIGN KEY (`fk_reservation`) REFERENCES `Reservation` (`pk_id`);

--
-- Contraintes pour la table `Reservation`
--
ALTER TABLE `Reservation`
  ADD CONSTRAINT `Reservation_ibfk_1` FOREIGN KEY (`fk_seance`) REFERENCES `Seance` (`pk_id`);

--
-- Contraintes pour la table `Seance`
--
ALTER TABLE `Seance`
  ADD CONSTRAINT `Seance_ibfk_1` FOREIGN KEY (`fk_atelier`) REFERENCES `Atelier` (`pk_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
