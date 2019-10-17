let params = new URL(document.location).searchParams;
var n = parseInt(params.get('n'));
var refresh = parseInt(params.get('refresh')) * 1000 || 40000;
var turn = parseInt(params.get('turn')) * 1000 || 20000;
var m = 0;

function s_index(atelier, horaire) {
    // 7 + (atelier + 1) + atelier * 7 + (horaire + 1);
    var n = 9 + 8 * atelier + horaire;
    return document.querySelector('body > div:nth-child(' + n + ')');
}

function update() {
    data = JSON.parse(window.localStorage.getItem('placesRestantesCache'))
    let i = 0;
    if (data.length > n) {
        if (n * m >= data.length) {
            m = 0;
        }
        data = data.slice(n * m, n + n * m);
        m++;
    }
    for (atelier of data) {
        s_index(i, -1).innerText = atelier[0];
        atelier[1].forEach(function (item, index) {
            s_index(i, index).innerText = item;
        });
        i ++;
    }
}

function refreshCache() {
    fetch(document.location.href, {
        headers: new Headers({'Accept': 'application/json'})
    })
    .then(res => res.json())
    .then(function (data) {
        window.localStorage.setItem('placesRestantesCache', JSON.stringify(data));
        console.log('Rafraichissement des données');
    })
    .catch(function (err) {
        console.log(err);
    });
}

refreshCache();
update(JSON.parse(window.localStorage.getItem('placesRestantesCache')));

window.setInterval(refreshCache, refresh);
window.setInterval(update, turn);
