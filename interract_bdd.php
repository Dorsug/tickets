<?php
/**
* Fichiers d'interraction entre script.js (via AJAX) et functions_bdd.php
* L'action a effectuer arriver par méthode GET.
* On peut donc appeler le(s) bon(nes) fonctions grace à un simple switch/case
*
*/

require("functions_bdd.php");

//Connection à la BdD
$bdd = connect_bdd();


if( isset($_GET['action'])) {
	switch ($_GET['action']){
		case "displayWorkshop":
			displayWorkshop($bdd);
			break;
			
		case "displayShedules":
			displayShedules($bdd);
			break;
		
		case "displaySessionByID":
			displaySessionByID($bdd,$_GET['id']);
			break;
			
		case "decrementAndReload":
			decrementAndReload($bdd,$_GET['id'],$_GET['idWorkshop']);
			break;
		
		case "addSessionToCart":
			addSessionToCart($bdd,$_GET['id'],$_GET['idWorkshop']);
			break;
		
		case "addPrice":
			getPriceBySessionID($bdd,$_GET['id']);
			break;
		
		case "removeSessionToCart":
			removeSessionToCart($bdd,$_GET['id']);
			break;
			
		case "reloadSessions":
			reloadSessions($bdd,$_GET['idWorkshop']);
			break;
			
			
		default:
	}

}
//Espace de test
/*

*/
?>
