var popupTimeout

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

function _updateCompteurPlaces(seanceId, add=1) {
    seance = document.querySelector(`.seance[data-id="${seanceId}"]`);
    seance.innerText = Number(seance.innerText) + add;
}

function _ajouterAuPanier(itemId, seanceId, horaire, atelier) {
    tmp1 = document.getElementById('panier_item-template').content.cloneNode(true);
    div = tmp1.querySelector('div');
    div.setAttribute('data-id', itemId);
    div.setAttribute('data-seance', seanceId);
    tmp1.querySelector('.titre').innerText = horaire;
    tmp1.querySelector('.content').innerText = atelier;

    document.querySelector('#panier').appendChild(tmp1);

    document.querySelector('#panierId').innerText = Cookies.get('panierId');
}

function ajouterAuPanier(obj){
    seanceId = obj.getAttribute('data-id');
    horaire = obj.getAttribute('data-horaire');
    atelier = obj.parentNode.getAttribute('data-atelier');

    fetch('/panier', {
        method: 'POST',
        body: new URLSearchParams({'seanceId': seanceId}),
    })
    .then((res) => _getData(res, 'json'))
    .then(function(data) {
        // Ajoute l'item dans le panier
        _ajouterAuPanier(data['itemId'], seanceId, horaire, atelier);
        // Décrémente de 1 le nombre de places dans l'interface
        obj.innerText = Number(obj.innerText) - 1;
    })
    .catch(function(err) {
        if (err.message == "410") {
            tmp1 = document.getElementById('popup_error-template').content.cloneNode(true);
            document.body.appendChild(tmp1);
            popupTimeout = setTimeout(function () { document.querySelector('.popup').remove();}, 3000);
        } else { console.log(err); }
    });
}

function enleverDuPanier(obj){
    panierItem = obj.parentNode;
    itemId = panierItem.getAttribute('data-id');
    seanceId = panierItem.getAttribute('data-seance');

    fetch('/panier', {
        method: "DELETE",
        body: new URLSearchParams({'itemId': itemId}),
    })
    .then((res) => _getData(res))
    .then(function(data){
        panierItem.remove();
        _updateCompteurPlaces(seanceId);
    })
    .catch(function(err) {
        console.log(err);
    });
}

function chargerPanier(panierId) {
    Cookies.set('panierId', panierId);
    window.location = '/?admin';
}

function viderPanier() {
    fetch('/panier', {method: "DELETE"})
    .then((res) => _getData(res))
    .then(function(data){
        panier = document.querySelector('#panier');
        for (item of panier.children) {
            _updateCompteurPlaces(item.getAttribute('data-seance'));
        }
        panier.innerHTML = "";
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
    document.querySelector('#panierId').innerText = '';
    document.querySelector('#panier .content').innerHTML = '';
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

function showReserver() {
    document.getElementById('reserver').style.display = 'block';
    _getCssRule('.pane').style.filter = 'blur(3px)';
}

function hideReserver() {
    document.getElementById('reserver').style.display = 'none';
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

function printPanier(panierId, el) {
    fetch('/impression/' + encodeURIComponent(panierId), {method: 'POST'})
    .then((res) => _getData(res))
    .then(function(data) {
        el.closest('.client').classList.add('printed');
    })
    .catch(function(err) {
        console.log(err);
    });
}

function selectDescription(el) {
    className = 'selected';
    el_descr = el.closest('.atelier').querySelector('.description');
    for (div of document.querySelectorAll('.atelier .description.selected') || []) {
        if (div != el_descr) {
            div.classList.remove(className);
        }
    }
    el_descr.classList.toggle('selected');

}

function selectDate(el) {
    Cookies.set('date', el.innerText);
    window.location.reload();
}

function selectPrinter(el) {
    Cookies.set('imprimante', el.innerText);
    select(el);
}

function showPage(el) {
    for (page of document.querySelectorAll('.page')) {
        page.style.display = 'none';
    }
    document.querySelector('.page[data-pagenumber = "' + el.dataset.pagenumber + '"]').style.display = 'block';

    for (page of document.querySelectorAll('.pageButton')) {
        page.style.backgroundColor = 'var(--c3)';
    }
    document.querySelector('.pageButton[data-pagenumber = "' + el.dataset.pagenumber + '"]').style.backgroundColor = 'white';
}

/* Run at application start to set defaults */

// Set the default
if (typeof Cookies.get('date') == 'undefined') {
    Cookies.set('date', 'Samedi');
}
/*
inputDate = document.querySelector('#pane1 .dates')
// Check the correct box
inputDate.querySelector('input[value="' + date + '"]').checked = true;
// Define callback to change when clicked
for (box of inputDate.querySelectorAll('input')) {
    box.onclick = function () {
        Cookies.set('date', this.value);
    };
}
*/

if (Cookies.get('panierId')) {
    fetch('/panier', {
        method: 'GET',
    })
    .then((res) => _getData(res, 'json'))
    .then(function(data) {
        for (item of data) {
            _ajouterAuPanier(item['id'], item['seance'], item['datetime'], item['atelier']);
        }
    })
    .catch(function(err) {
        console.log(err);
    });
}
