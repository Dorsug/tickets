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
		echo "<p style=\"background-color : red;\";>";
			echo "<strong>" . $donnees['nom'] . "</strong><br />"; 
			echo $donnees['description'] . "<br />"; 
			echo $donnees['agemini'] . " - " . $donnees['agemaxi'] . "<br />"; 
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
?>