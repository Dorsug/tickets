<?php
require("functions_bdd.php");

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
			
		case "addSessionToCart":
			addSessionToCart($bdd,$_GET['id'],$_GET['idWorkshop']);
			break;
		
		default:
	}

}
//Espace de test
/*

*/
?>
