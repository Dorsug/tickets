inputDate = document.querySelector('#pane1 .dates')
// Set the default
date = Cookies.get('date');
if (typeof date == 'undefined') {
    Cookies.set('date', 'samedi');
    date = 'samedi';
}
// Check the correct box
inputDate.querySelector('input[value="' + date + '"]').checked = true;
// Define callback to change when clicked
for (box of inputDate.querySelectorAll('input')) {
    box.onclick = function () { 
        Cookies.set('date', this.value);
    };
}


function _getData(res, format='text') {
    if(res.ok) {
        if (format == 'text') {
            return res.text();
        } else if (format == 'json') {
            return res.json();
        }
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

function ajouterAuPanier(obj){
    seanceId = obj.getAttribute('data-id');
    horaire = obj.getAttribute('data-horaire');
    atelier = obj.parentNode.getAttribute('data-atelier');

    container = document.querySelector('#panier .content');

    fetch('/panier', {
        method: 'POST',
        body: new URLSearchParams({'seanceId': seanceId}),
    })
    .then((res) => _getData(res, 'json'))
    .then(function(data) {
        tmp1 = document.getElementById('panier_item-template').content.cloneNode(true);
        tmp1.querySelector('div').setAttribute('data-id', data['itemId']);
        tmp1.querySelector('.titre').innerText = horaire;
        tmp1.querySelector('.content').innerText = atelier;
        container.appendChild(tmp1);
    })
    .catch(function(err) {
        console.log(err);
    });
}

function enleverDuPanier(obj){
    panierItem = obj.parentNode;
    itemId = panierItem.getAttribute('data-id');

    fetch('/panier', {
        method: "DELETE",
        body: new URLSearchParams({'itemId': itemId}),
    })
    .then((res) => _getData(res))
    .then(function(data){
        panierItem.remove();
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

function showReservationContent(panierId, el) {
    fetch('/panier/' + encodeURIComponent(panierId))
    .then((res) => _getData(res))
    .then(function(data) {
        try {
            document.querySelector('#pane2 .selected').classList.remove('selected');
        } catch (e) {}
        el.classList.add('selected');
        document.querySelector('#pane3 .content').innerHTML = data;
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

function impression() {
    document.querySelector('.loader').style.display = 'block';
}
