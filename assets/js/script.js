$(function(){
    $('button').on('click',function(){       
        switch ($(this).html()) {
            case 'Ateliers':
                document.getElementById('pane1Title').innerHTML = "Ateliers";
                document.getElementById('pane2Title').innerHTML = "Horaires";
                console.log("Bouton \"Ateliers\" pressé");
                break;
                
            case 'Horaires':
                document.getElementById('pane1Title').innerHTML = "Horaires";
                document.getElementById('pane2Title').innerHTML = "Ateliers";
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

