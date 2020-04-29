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
