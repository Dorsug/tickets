<?php
/**
* Fichiers d'interraction avec la BdD.
* Ses fonctions sont appelés dans script.js via (AJAX) interract_bdd.php
* La reponse (ce qu'on veut afficher) doit passer par des 'echo' pour que les fonctions JS puissent l'afficher
*
*/


//Connection à la BdDs
function connect_bdd(){
	try{
		return $bdd = new PDO('mysql:host=localhost;dbname=gestickets2_bdd;charset=utf8', 'root', '');
	}catch (Exception $e){
		die('Erreur : ' . $e->getMessage());
	}
}

//Affichage des ateliers
function displayWorkshop ($bdd){
	$reponse = $bdd->query('SELECT * 
							FROM `atelier`');
	//Affichage des ateliers
	while ($donnees = $reponse->fetch()){
		if(!workshopIsEmpty($bdd,$donnees['numero'])){
			echo "<p onclick=\"displaySession( " . $donnees['numero'] . ");\" style=\"cursor: pointer;background-color: #999;border-radius: 5px;\";>";
				echo "<strong>" . $donnees['numero'] . " - " . $donnees['nom'] . "</strong><br />"; 
				echo $donnees['description'] . "<br />"; 
				echo "Age : " . $donnees['agemini'] . " - " . $donnees['agemaxi'] . "<br />"; 
				echo $donnees['prix'] . "€"; 
			echo "</p>";
		}
	}
	$reponse->closeCursor();
}

//Atelier vide ?
function workshopIsEmpty($bdd,$id){
	//Recuperation des sessions d'un ateliers dont le nombre de places restantes est supérieur à 0 
	$reponse = $bdd->query('SELECT pk_id, fk_atelier, DATE_FORMAT(date, \'%d/%m\') AS dateSession, DATE_FORMAT(heureDebut, \'%Hh%i\') AS heureDebut, DATE_FORMAT(heureFin, \'%Hh%i\') AS heureFin, nbrPlace 
							FROM `seance` 
							WHERE fk_atelier = ' . $id . '&& date>=NOW() && nbrPlace>0');
	$isEmpty = true;
	
	//Si on recupere au moins un atelier -> il n'est pas vide
	while ($donnees = $reponse->fetch()){
		$isEmpty= false;
	}
	$reponse->closeCursor();
	
	return $isEmpty;
}

//Affichage des horaires - ToDo
function displayShedules ($bdd){
	$reponse = $bdd->query('SELECT * 
							FROM `seance`');

	while ($donnees = $reponse->fetch()){
		echo "<p style=\"cursor: pointer;background-color: #777;border-radius: 5px;\";>";
			echo "<strong>" . $donnees['date'] . "</strong><br />"; 
			echo $donnees['heureDebut'] . " - " . $donnees['heureFin'] . "<br />"; 
			echo "Atelier " . $donnees['fk_atelier'];
		echo "</p>";
	}
	$reponse->closeCursor();
}

//Affichage des sessions pour un atelier donné ($id)
function displaySessionByID($bdd, $id){
	//On demande à la BdD les sessions lié à l'atelier n°$id qui ne sont pas encore passé et qui ne sont pas vide
	$reponse = $bdd->query('SELECT pk_id, fk_atelier, DATE_FORMAT(date, \'%d/%m\') AS dateSession, DATE_FORMAT(heureDebut, \'%Hh%i\') AS heureDebut, DATE_FORMAT(heureFin, \'%Hh%i\') AS heureFin, nbrPlace 
							FROM `seance` 
							WHERE fk_atelier = ' . $id . '&& date>=NOW() && nbrPlace>0');

	//Affichage de l'atelier
	while ($donnees = $reponse->fetch()){
		echo "<p onclick=\"addToCart(" . $donnees['pk_id'] . "," . $donnees['fk_atelier'] . ");\" style=\"cursor: pointer;background-color: #777;border-radius: 5px;\" >";
			echo "<strong>" . $donnees['dateSession'] . "</strong><br />"; 
			echo $donnees['heureDebut'] . " - " . $donnees['heureFin'] . "<br />";
			echo "<i>Places restantes : " . $donnees['nbrPlace'] . "</i>";
		echo "</p>";
	}
	$reponse->closeCursor();
}

//Suppression d'une place d'une session
function decrementAndReload($bdd, $id, $idWorkshopSelect){
	//On decremente d'un le nombre de place disponible sur l'atelier
	$bdd->query('UPDATE `seance` 
				SET nbrPlace=nbrPlace-1 
				WHERE pk_id=' . $id);
	
	//Mise à jour de l'affichage
	displaySessionByID($bdd, $idWorkshopSelect);
}

//Ajout d'une session au panier
function addSessionToCart($bdd, $id, $idWorkshopSelect){
	//On recupere les infos de l'atelier 
	$reponse = $bdd->query("SELECT atelier.nom, seance.pk_id AS id, seance.*
							FROM atelier, seance
							WHERE fk_atelier=numero && seance.pk_id=" . $id);
	$donnees = $reponse->fetch();
	
	//Affichage des infos de l'atelier + bouton de suppression du panier dans le panier
	echo "<span><span class=\"removeSession\" style=\"cursor: pointer;display: inline-block;\" onclick=\"removeSessionToCart(" . $donnees["id"] . ",this);\">✖</span>  <strong>" . $donnees['nom'] . " </strong>- " . date_format(date_create($donnees['date']),'m/d') . " (" . date_format(date_create($donnees['heureDebut']),'H:i') . " -" . date_format(date_create($donnees['heureFin']),'H:i') . ")<br /></span>";
	
}

//Suppression d'une session du panier
function removeSessionToCart($bdd,$id){
	//Ajout de nombre de place disponible de 1
	$bdd->query("UPDATE `seance` 
				SET `nbrPlace`=nbrPlace+1 
				WHERE pk_id=" . $id);
}

//Recuperation du prix d'une session
function getPriceBySessionID($bdd, $id){
	$reponse = $bdd->query("SELECT prix
							FROM atelier 
							WHERE numero = (SELECT fk_atelier 
											FROM seance  
											WHERE pk_id =" . $id . ")");
	$donnees = $reponse->fetch();
	
	//On renvoit le prix
	echo $donnees["prix"];
	
}

//Mise à jour de l'affichage des sessions
function reloadSessions($bdd,$id){
	displaySessionByID($bdd, $id);
}

?>