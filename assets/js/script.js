inputDate = document.querySelector('#pane1 .dates')
// Set the default
date = Cookies.get('date');
if (typeof date == 'undefined') {
    Cookies.set('date', 'Samedi');
    date = 'Samedi';
}
// Check the correct box
inputDate.querySelector('input[value="' + date + '"]').checked = true;
// Define callback to change when clicked
for (box of inputDate.querySelectorAll('input')) {
    box.onclick = function () { 
        Cookies.set('date', this.value);
    };
}


function _getData(res) {
    if(res.ok) {
        return res.text()
    } else {
        throw new Error(res.status);
    }
}

function _getCssRule(rule) {
    let cssRules = [...document.styleSheets[0].cssRules];
    cssRule = cssRules.find((x) => { return x.selectorText == rule } )
    if (typeof(cssRule) == 'undefined') {
        document.styleSheets[0].insertRule(rule + '{}', 0);
        cssRule = document.styleSheets[0].cssRules[0];
    }
    return cssRule
}


function listerAteliers() {
    fetch('/ateliers')
    .then((res) => _getData(res))
    .then(function(data){
        // Modifications esthétiques
            // Change la disposition des colonnes 2 et 3
            document.getElementById('pane3').style.display = '';
            document.getElementById('pane2').style['grid-column'] = '2 / span 1';
            // Change les classe 'selected' dans la colonne 1
            try {
                document.querySelector('#pane1 .selected').classList.remove('selected');
            } catch (e) {}
            try {
                document.querySelector('#pane1 .horaires > .selected').classList.remove('selected');
            } catch (e) {}
            document.querySelector('#pane1 .ateliers').classList.add('selected');
        // Remplissage des données
        document.querySelector('#pane2 .content').innerHTML = data;
    })
    .catch(function(err) {
        console.log(err);
    });
}

function listerReservations() {
    fetch('/reservations')
    .then((res) => _getData(res))
    .then(function(data) {
        // Modifications esthétiques
            // Change la disposition des colonnes 2 et 3
            document.getElementById('pane3').style.display = '';
            document.getElementById('pane2').style['grid-column'] = '2 / span 1';
            // Change les classe 'selected' dans la colonne 1
            try {
                document.querySelector('#pane1 .selected').classList.remove('selected');
            } catch (e) {}
            try {
                document.querySelector('#pane1 .horaires > .selected').classList.remove('selected');
            } catch (e) {}
            document.querySelector('#pane1 .reservations').classList.add('selected');
            document.querySelector('#pane3 .content').innerHTML = '';
        // Remplissage des données
        document.querySelector('#pane2 .content').innerHTML = data;
    })
    .catch(function(err) {
        console.log(err);
    });
}

function listerSeances(element, atelierId){
    fetch('/seances?atelierId=' + encodeURIComponent(atelierId))
    .then((res) => _getData(res))
    .then(function(data){
        // Modifications esthétiques
        try {
            document.querySelector('#pane2 .selected').classList.remove('selected')
        } catch (e) {}
        element.classList.add('selected');
        // Remplissage des données
        document.querySelector("#pane3 .content").innerHTML = data;
    })
    .catch(function(err) {
        console.log(err);
    });
}

function listerSeancesPourHoraire(element, horaire) {
    fetch('/seances?horaire=' + encodeURIComponent(horaire))
    .then((res) => _getData(res))
    .then(function(data) {
        // Modifications esthétiques
            // Change la disposition des colonnes 2 et 3
            document.getElementById('pane3').style.display = 'none';
            document.getElementById('pane2').style['grid-column'] = '2 / span 2';
            // Change les classe 'selected' dans la colonne 1
            try {
                document.querySelector('#pane1 .selected').classList.remove('selected');
            } catch (e) {}
            try {
                document.querySelector('#pane1 .horaires > .selected').classList.remove('selected');
            } catch (e) {}
            document.querySelector('#pane1 .horaires').classList.add('selected');
            element.classList.add('selected');
        // Remplissage des données
        document.querySelector('#pane2 .content').innerHTML = data;
    })
    .catch(function(err) {
        console.log(err);
    });
}

function majInterfacePanier() {
    fetch('/panier')
    .then((res) => _getData(res))
    .then(function(data) {
        document.querySelector('#pane4 .content').innerHTML = data;
    })
    .catch(function(err) {
        console.log(err);
    });
}

function ajouterAuPanier(seanceId){
    fetch('/panier', {
        method: 'POST',
        body: new URLSearchParams({'seanceId': seanceId}),
    })
    .then((res) => _getData(res))
    .then(function(data) {
        majInterfacePanier();
    })
    .catch(function(err) {
        console.log(err);
    });
}

function enleverDuPanier(seanceId){
    fetch('/panier', {
        method: "DELETE",
        body: new URLSearchParams({'seanceId': seanceId}),
    })
    .then((res) => _getData(res))
    .then(function(data){
        majInterfacePanier();
    })
    .catch(function(err) {
        console.log(err);
    });
}

function viderPanier() {
    fetch('/panier', {method: "DELETE"})
    .then((res) => _getData(res))
    .then(function(data){
        majInterfacePanier();
    })
    .catch(function(err) {
        console.log(err);
    });
}

function resaSearch() {
    var filter = document.getElementById('resaSearchBar').value.toUpperCase();
    elements = document.querySelectorAll('#pane2 .bulle');
    for (i = 0; i < elements.length; i++) {
        txtValue = elements[i].textContent || elements[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            elements[i].style.display = "";
        } else {
            elements[i].style.display = "none";
        }
    }
}

function showReservationContent(panierId) {
    fetch('/panier/' + encodeURIComponent(panierId))
    .then((res) => _getData(res))
    .then(function(data) {
        document.querySelector('#pane3 .content').innerHTML = data;
        console.log(data);
    })
    .catch(function(err) {
        console.log(err);
    });
}

function setPrinter(printer) {
    Cookies.set('imprimante', printer);
}

function setNouveauPanier() {
    Cookies.remove('panierId');
    document.querySelector('#pane4 .content').innerHTML = '';
}

function getPanierPrecedent() {
    paniers = JSON.parse(localStorage.getItem('paniers'));
    window.location = '/panier/' + paniers[0];
}

function showPaiement() {
    document.getElementById('paiement').style.display = 'block';
    _getCssRule('.pane').style.filter = 'blur(3px)';
}

function hidePaiement() {
    document.getElementById('paiement').style.display = 'none';
    _getCssRule('.pane').style.filter = '';
}

function paiement() {
    // Fait apparaitre le 'loader'
    document.querySelector('.loader').style.display = 'block';

    // Enregistre le panier dans le localStorage
    panier_current = Cookies.get('panierId')
    paniers_historic = JSON.parse(localStorage.getItem('paniers')) || new Array;
    paniers_historic.unshift(panier_current)
    localStorage.setItem('paniers', JSON.stringify(paniers_historic))
}
