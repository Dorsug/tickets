//Global Variable
idWorkshopSelected = 0;
listOfSession = [];

//Functions

//Ecouteur du click sur les boutons 
$(function(){
    $('button').on('click',function(){      
        switch ($(this).html()) {
            case 'Ateliers':
                document.getElementById('pane1Title').innerHTML = "Ateliers";
                document.getElementById('pane2Title').innerHTML = "Horaires";
				document.getElementById('pane2Div').innerHTML = "";
				
				//Affichage des Ateliers
				$.get(
					'interract_bdd.php', 
					{action : "displayWorkshop"},
					function(data){
						$("#pane1Div").html(data);
					},
					'text'
				 );
				
                console.log("Bouton \"Ateliers\" pressé");
                break;
                
            case 'Horaires':
                document.getElementById('pane1Title').innerHTML = "Horaires";
                document.getElementById('pane2Title').innerHTML = "Ateliers";
				document.getElementById('pane2Div').innerHTML = "";
				
				//Affichages des Horaires
				$.get(
					'interract_bdd.php', 
					{action : "displayShedules"},
					function(data){
						$("#pane1Div").html(data);
					},
					'text'
				 );
				
                console.log("Bouton \"Horaires\" pressé");
                break;
                
            case 'Reservations':
                document.getElementById('pane1Title').innerHTML = "Reservations";
                document.getElementById('pane2Title').innerHTML = "";  
                console.log("Bouton \"Reservations\" pressé");
                break;
                
            case 'Effacer':
                console.log("Bouton \"Effacer\" pressé");
				console.log(listOfSession.toString());
				for(i=0; i <listOfSession.length; i++){
					$.get(
						'interract_bdd.php', 
						{
							action : "removeSessionToCart",
							id : listOfSession[i]
						},
						function(data){
							//Supprimer la session du panier
						},
						'text'
					);
				}
				listOfSession.splice(0,listOfSession.length);
				//Mise à jour de l'affichage
				$.get(
					'interract_bdd.php', 
					{
						action : "reloadSessions",
						idWorkshop : idWorkshopSelected
					},
					function(data){
						$("#pane2Div").html(data);
					},
					'text'
				);
				
				document.getElementById("total").innerHTML="0";
				document.getElementById("briefWorkshop").innerHTML="";
                break;
                
            case 'Paiement':
                console.log("Bouton \"Paiement\" pressé");
                break;
                
            default:
                console.log("default");
        }
    });
  });
  
//Affichage des horaires pour un atelier selectionné
function displaySession(idWorkshop){
	console.log("Atelier " + idWorkshop);
	idWorkshopSelected=idWorkshop;
	
	$.get(
		'interract_bdd.php', 
		{
			action : "displaySessionByID",
			id : idWorkshop
		},
		function(data){
			$("#pane2Div").html(data);
			if(data == ""){
				$("#pane2Div").html("Il n'y a plus de sessions disponible pour cet atelier.");
			}
		},
		'text'
	);
}

//Ajout d'une session d'un atelier dans le panier
function addToCart(idSession, idWorkshop){
	console.log("Session " + idSession);
	listOfSession.push(idSession);
	
	//On diminue le nombre de place de la session de 1 et on met à jour l'affichage
	$.get(
		'interract_bdd.php', 
		{
			action : "decrementAndReload",
			id : idSession,
			idWorkshop : idWorkshopSelected 
		},
		function(data){
			$("#pane2Div").html(data);
		},
		'text'
	);
	
	//On ajoute la session dans le recap du panier
	$.get(
		'interract_bdd.php', 
		{
			action : "addSessionToCart",
			id : idSession,
			idWorkshop : idWorkshop
		},
		function(data){
			$("#briefWorkshop").html($("#briefWorkshop").html()+data);
		},
		'text'
	);
	
	//On met à jour le prix
	$.get(
		'interract_bdd.php', 
		{
			action : "addPrice",
			id : idSession
		},
		function(data){
			$("#total").html((Number($("#total").html())+Number(data)).toFixed(2));
		},
		'text'
	);
	
}
 
//Suppression d'une session d'un atelier dans le panier
function removeSessionToCart(idSession,idElt){
	//Supprimer la session de la liste
	for(i=0; i <listOfSession.length; i++){
		if(listOfSession[i]==idSession){
			listOfSession.splice(i,1);
			break;
		}
	}
	
	$.get(
		'interract_bdd.php', 
		{
			action : "removeSessionToCart",
			id : idSession
		},
		function(data){
			//Supprimer la session du panier
		},
		'text'
	);
	idElt.parentElement.innerHTML=""; //Suppression de la session dans l'affichage du panier
	
	//Mise à jour de l'affichage
	$.get(
		'interract_bdd.php', 
		{
			action : "reloadSessions",
			idWorkshop : idWorkshopSelected
		},
		function(data){
			$("#pane2Div").html(data);
		},
		'text'
	);
	//Mise à jour du prix
	$.get(
		'interract_bdd.php', 
		{
			action : "addPrice",
			id : idSession
		},
		function(data){
			$("#total").html((Number($("#total").html())-Number(data)).toFixed(2));
		},
		'text'
	);
	
	
}  