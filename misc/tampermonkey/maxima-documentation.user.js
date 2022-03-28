// ==UserScript==
// @name         Maxima documentation
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Make the Maxima documentation a bit easier on the eyes.
// @author       Alexander E. Zarebski
// @match        https://maxima.sourceforge.io/docs/manual/*
// @grant        none
// ==/UserScript==

const space = {
    yellow: "#b1951d",
    lightYellow: "#f6f1e1",
    lightLightYellow: "#fbf8ef",
    orangeText: "#da8b55",
    blueHeadings: "#3a81c3",
    aqua: "#2d9574",
    cyan: "#21b8c7",
    tealLinks: "#2aa1ae",
    redBackground: "#eed9d2",
    redWarning: "#f2241f",
    redBorder: "#ba2f59",
    purpleBackgroundLight: "#ddd8eb",
    purpleBackgroundDark: "#9380b2",
    purpleTextBright: "#a31db1",
    purpleText: "#4e3163",
    purpleTitle: "#6c3163"
};

const tagsHaveColor = (tagName,colorHex) => {
    Array.from(document.getElementsByTagName(tagName)).forEach((e) => {e.style.color = colorHex;});
};

(function() {
    'use strict';

    document.body.style.fontSize = "27px";
    document.body.style.background = space.lightLightYellow;
    document.body.style.color = space.purpleText;
    tagsHaveColor("h1", space.blueHeadings);
    tagsHaveColor("h2", space.blueHeadings);
    tagsHaveColor("h3", space.blueHeadings);
    tagsHaveColor("h4", space.blueHeadings);
    tagsHaveColor("a", space.tealLinks);
})();
