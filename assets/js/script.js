$(function(){
    $('button').on('click',function(){      
        switch ($(this).html()) {
            case 'Ateliers':
                document.getElementById('pane1Title').innerHTML = "Ateliers";
                document.getElementById('pane2Title').innerHTML = "Horaires";
				document.getElementById('pane2Div').innerHTML = "";
				
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
                break;
                
            case 'Paiement':
                console.log("Bouton \"Paiement\" pressé");
                break;
                
            default:
                console.log("default");
        }
    });
  });
  
function displaySession(idWorkshop){
	console.log("Atelier " + idWorkshop);
	$.get(
		'interract_bdd.php', 
		{
			action : "displaySessionByID",
			id : idWorkshop
		},
		function(data){
			$("#pane2Div").html(data);
		},
		'text'
	);
}

function addToCart(idSession, idWorkshop){
	console.log("Session " + idSession);
	$.get(
		'interract_bdd.php', 
		{
			action : "addSessionToCart",
			id : idSession,
			idWorkshop : idWorkshop
		},
		function(data){
			$("#pane2Div").html(data);
		},
		'text'
	);
}
  

function getXMLHttpRequest() {
	var xhr = null;
	
	if (window.XMLHttpRequest || window.ActiveXObject) {
		if (window.ActiveXObject) {
			try {
				xhr = new ActiveXObject("Msxml2.XMLHTTP");
			} catch(e) {
				xhr = new ActiveXObject("Microsoft.XMLHTTP");
			}
		} else {
			xhr = new XMLHttpRequest(); 
		}
	} else {
		alert("Votre navigateur ne supporte pas l'objet XMLHTTPRequest...");
		return null;
	}
	
	return xhr;
}