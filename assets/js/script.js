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

function majInterfacePanier(panierId) {
    $.ajax({
        url: "/panier",
        data: {
            'action': 'lister',
            'panierId': panierId
        },
        success: function(data){
            document.querySelector('#panier .ateliers .list').innerHTML = data;
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
            majInterfacePanier(panierId);
        },
        error: function(req, status, error){
            console.log(error);
        }
    });
}

function enleverDuPanier(seanceId){
    panierId = Cookies.get('panierId');
    $.ajax({
        method: "DELETE",
        url: "/panier",
        data: {
            'panierId': panierId,
            'seanceId': seanceId,
        },
        success: function(data){
            majInterfacePanier(panierId);
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
