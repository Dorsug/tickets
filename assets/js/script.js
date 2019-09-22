function listerAteliers() {
    document.getElementById('pane1Title').innerHTML = "Ateliers";
    document.getElementById('pane2Title').innerHTML = "Horaires";
    document.getElementById('pane2Div').innerHTML = "";
                
    $.ajax({
        url: '/ateliers', 
        success: function(data){
            $("#pane1Div").html(data);
        }
    });
}

function listerHoraires() {
    document.getElementById('pane1Title').innerHTML = "Horaires";
    document.getElementById('pane2Title').innerHTML = "Ateliers";
    document.getElementById('pane2Div').innerHTML = ""; // Reset de la seconde pane

    $.ajax({
        url: '/horaires', 
        success: function(data){
            $("#pane1Div").html(data);
        },
    });
}

function listerReservations() {
    document.getElementById('pane1Title').innerHTML = "Reservations";
    document.getElementById('pane2Title').innerHTML = "";  
    // TODO
}

function listerSeances(atelierId){
    $.ajax({
        url: '/seances', 
        data: { 'atelierId': atelierId },
        success: function(data){
            $("#pane2Div").html(data);
            if(data == ""){ //Cas où l'atelier n'a plus de sessions disponibles
                $("#pane2Div").html("Il n'y a plus de sessions disponible pour cet atelier.");
            }
        }
    });
}

function ajouterAuPanier(seanceId){
    panierId = Cookies.get('panierId');
    $.ajax({
        method: "POST",
        url: "/panier",
        data: {
            'action': 'ajouter',
            'panierId': panierId,
            'seanceId': seanceId,
        },
        success: function(data){
            console.log('Seance ajouté au panier');
            console.log(data);
        },
        error: function(req, status, error){
            console.log(error);
        }
    });
}

function getPanierId(){
    $.ajax({
        url:'/panier', 
        data: {'action': 'new'}, 
        success: function(data){
            Cookies.set('panierId', data);
        }
    });
}

/*
            case 'Effacer':
                console.log("Bouton \"Effacer\" pressé");
				
				//On supprime session par session les sessions du panier
				for(i=0; i <listOfSession.length; i++){
					$.get(
						'interract_bdd.php', 
						{
							action : "removeSessionToCart",
							id : listOfSession[i]
						},
						function(data){
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
				
				//On vide l'affichage du panier et du prix
				document.getElementById("total").innerHTML="0";
				document.getElementById("briefWorkshop").innerHTML="";
                break;
                
			//Click sur le bouton Paiement - Ne marche pas car Paiement est un lien et non un bouton	
            case 'Paiement':
                console.log("Bouton \"Paiement\" pressé");
                break;
                
            default:
                console.log("default");
        }
    });
  });
*/

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

//Recuperation des valeurs du formulaire de paiement
function submitForm(sessionID){
	console.log(sessionID);
	//Recuperation de la valeur "Mode de Paiement"
	var paymentMode
    var inputs = document.getElementsByTagName('input'),
        inputsLength = inputs.length;

    for (var i = 0; i < inputsLength; i++) {
        if (inputs[i].type === 'radio' && inputs[i].checked) {
			paymentMode=inputs[i].value;
            console.log(inputs[i].value + " selectionné");
        }
    }
	//Recuperation du code postal
	console.log(document.getElementById("postalCodeForm").value);
	
	//Requete AJAX
	$.get(
		'generate_pdf.php', 
		{
			sessionID : sessionID,												//ID de session
			paymentMode : paymentMode, 											//Mode de paiement
			postalCode : document.getElementById("postalCodeForm").value,		//Code Postal
			totalPrice : Number($("#total").html()),						    //Prix
			listOfSession : listOfSession										//Liste des ateliers
			
		},
		function(data){
			window.open('./data/'+sessionID+'.pdf', '_blank');						//Affichage de la facture
		},
		'text'
	);
	console.log("Etiquette générée");
	
}
