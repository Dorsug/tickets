<?php
require("functions_bdd.php");

$bdd = connect_bdd();

if( isset($_POST['action'])) {
	switch ($_POST['action']){
		case "displayWorkshop":
			displayWorkshop($bdd);
			break;
			
		case "displayShedules":
			displayShedules($bdd);
			break;
			
		default:
	}

}
//Espace de test
/*

*/
?>
