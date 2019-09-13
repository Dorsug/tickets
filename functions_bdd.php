<?php
function connect_bdd(){
	try{
		return $bdd = new PDO('mysql:host=localhost;dbname=gestickets2_bdd;charset=utf8', 'root', '');
	}catch (Exception $e){
		die('Erreur : ' . $e->getMessage());
	}
}

function displayWorkshop ($bdd){
	$reponse = $bdd->query('SELECT * FROM `atelier`');

	while ($donnees = $reponse->fetch()){
		echo "<p onclick=\"displaySession( " . $donnees['numero'] . ");\" style=\"background-color : red;\";>";
			echo "<strong>" . $donnees['nom'] . "</strong><br />"; 
			echo $donnees['description'] . "<br />"; 
			echo "Age : " . $donnees['agemini'] . " - " . $donnees['agemaxi'] . "<br />"; 
			echo $donnees['prix'] . "€"; 
		echo "</p>";
	}
	$reponse->closeCursor();
}

function displayShedules ($bdd){
	$reponse = $bdd->query('SELECT * FROM `seance`');

	while ($donnees = $reponse->fetch()){
		echo "<p style=\"background-color : green;\";>";
			echo "<strong>" . $donnees['date'] . "</strong><br />"; 
			echo $donnees['heureDebut'] . " - " . $donnees['heureFin'] . "<br />"; 
			echo "Atelier " . $donnees['fk_atelier'];
		echo "</p>";
	}
	$reponse->closeCursor();
}

function displaySessionByID($bdd, $id){
	$reponse = $bdd->query('SELECT pk_id, fk_atelier, DATE_FORMAT(date, \'%d/%m\') AS dateSession, DATE_FORMAT(heureDebut, \'%Hh%i\') AS heureDebut, DATE_FORMAT(heureFin, \'%Hh%i\') AS heureFin, nbrPlace FROM `seance` WHERE fk_atelier = ' . $id . '&& date>=NOW() && nbrPlace>0');

	while ($donnees = $reponse->fetch()){
		echo "<p onclick=\"addToCart(" . $donnees['pk_id'] . "," . $donnees['fk_atelier'] . ");\" style=\"background-color : green;\";>";
			echo "<strong>" . $donnees['dateSession'] . "</strong><br />"; 
			echo $donnees['heureDebut'] . " - " . $donnees['heureFin'] . "<br />";
			echo "<i>Places restantes : " . $donnees['nbrPlace'] . "</i>";
		echo "</p>";
	}
	$reponse->closeCursor();
}

function addSessionToCart($bdd, $id, $idWorkshopSelect){
	$bdd->query('UPDATE `seance` SET nbrPlace=nbrPlace-1 WHERE pk_id=' . $id);
	displaySessionByID($bdd, $idWorkshopSelect);
}

?>