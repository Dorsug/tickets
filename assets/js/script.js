function listerAteliers() {
    document.querySelector('#pane2 h1').innerHTML = "Ateliers";
    document.querySelector('#pane3 h1').innerHTML = "Horaires";
    document.querySelector('#pane3 .content').innerHTML = "";
                
    $.ajax({
        url: '/ateliers', 
        success: function(data){
            $("#pane2 .content").html(data);
        }
    });
}

function listerHoraires() {
    document.querySelector('#pane2 h1').innerHTML = "Horaires";
    document.querySelector('#pane3 h1').innerHTML = "Ateliers"; 
    document.querySelector('#pane3 .content').innerHTML = "";

    $.ajax({
        url: '/horaires', 
        success: function(data){
            $("#pane2 .content").html(data);
        },
    });
}

function listerReservations() {
    document.querySelector('#pane2 h1').innerHTML = "Reservations";
    document.querySelector('#pane3 h1').innerHTML = ""; 
    document.querySelector('#pane3 .content').innerHTML = "";
    // TODO
}

function listerSeances(atelierId){
    $.ajax({
        url: '/seances', 
        data: { 'atelierId': atelierId },
        success: function(data){
            $("#pane3 .content").html(data);
            if(data == ""){ //Cas où l'atelier n'a plus de sessions disponibles
                $("#pane3 .content").html("Il n'y a plus de sessions disponible pour cet atelier.");
            }
        }
    });
}

function majInterfacePanier() {
    $.ajax({
        url: "/panier",
        data: {
            'action': 'lister',
        },
        success: function(data){
            document.querySelector('#pane3 .content').innerHTML = data;
        }
    });
}

function ajouterAuPanier(seanceId){
    $.ajax({
        method: "POST",
        url: "/panier",
        data: {
            'seanceId': seanceId,
        },
        success: function(data){
            if(Cookies.get('panierId') != data){
                Cookies.set('panierId', data)
            };
            majInterfacePanier();
        },
        error: function(req, status, error){
            console.log(error);
        }
    });
}

function enleverDuPanier(seanceId){
    $.ajax({
        method: "DELETE",
        url: "/panier",
        data: {
            'seanceId': seanceId,
        },
        success: function(data){
            majInterfacePanier();
        },
        error: function(req, status, error){
            console.log(error);
        }
    });
}

function viderPanier() {
    $.ajax({
        method: "DELETE",
        url: "/panier",
        data: {},
        success: function(data){
            majInterfacePanier();
        },
        error: function(req, status, error){
            console.log(error);
        }
    });
}

function getChecked() {
    data = {'atelier': [], 'age': []};
    for (checkbox of document.querySelectorAll('input[type="checkbox"]')) {
        if (checkbox.checked == true) {
            data[checkbox.name].push(checkbox.value);
        }
    }
    data['heure'] = document.querySelector('#pane1 input[type="radio"][name="heure"]:checked').value
    data['date'] = document.querySelector('#pane1 input[type="radio"][name="date"]:checked').value
    return data
}

function getSeances() {
    $.ajax({
        method: 'POST',
        url: '/',
        data: JSON.stringify(getChecked()),
        contentType: 'application/json; charset=utf-8',
        success: function(data){
            document.querySelector('#pane2 .content').innerHTML = data;
        },
        error: function(req, status, error){
            console.log(req, status, error);
        }
    });
}
