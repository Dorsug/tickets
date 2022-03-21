let searchParams = new URLSearchParams(window.location.search);

function nextPage() {
    // /!\ works only for two pages
    const l = window.location;
    searchParams = new URLSearchParams(window.location.search);
    if (searchParams.get('page') == '1') {
        searchParams.set('page', '0');
    } else {
        searchParams.set('page', '1');
    }
    window.location = l.origin + l.pathname + '?' + searchParams.toString();
}

var refreshInterval_seconds = parseInt(searchParams.get('refresh'));
if (isNaN(refreshInterval_seconds)) {
    refreshInterval_seconds = 20;
}

window.setInterval(nextPage, refreshInterval_seconds * 1000);
