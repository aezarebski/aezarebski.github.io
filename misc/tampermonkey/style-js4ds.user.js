// ==UserScript==
// @name         Style JS4DS
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Make the site a little easier on the eye.
// @author       Alexander E Zarebski
// @match        http://js4ds.org/
// @match        https://js4ds.org/
// @icon         https://www.google.com/s2/favicons?domain=js4ds.org
// @grant        none
// ==/UserScript==

const tagsHaveColor = (tagName,colorHex) => {
        Array.from(document.getElementsByTagName(tagName)).forEach((e) => {e.style.color = colorHex;});
};

(function() {
    'use strict';
    document.body.style.fontSize = "20px";
    document.body.style.color = "#4e3163";
    document.body.style.backgroundColor = "#f6f1e1";
    tagsHaveColor("h1", "#3a81c3");
    tagsHaveColor("h2", "#3a81c3");
    tagsHaveColor("h3", "#3a81c3");
    tagsHaveColor("h4", "#3a81c3");
})();
