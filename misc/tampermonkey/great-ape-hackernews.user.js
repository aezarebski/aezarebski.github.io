// ==UserScript==
// @name         Hackernews
// @namespace    http://tampermonkey.net/
// @version      0.1.1
// @description  Make Hackernews a bit more friendly.
// @author       Alexander E. Zarebski
// @match        https://news.ycombinator.com/
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
    purpleTitle: "#6c3163",
    mediumFontSize: "18pt"
};

const tagsHaveColor = (tagName,colorHex) => {
    Array.from(document.getElementsByTagName(tagName)).forEach((e) => {e.style.color = colorHex;});
};

(function() {
    'use strict';
    document.body.style.backgroundColor = space.lightLightYellow;
    Array.from(document.getElementsByTagName("tbody")).forEach((e) => {e.style.backgroundColor = space.lightYellow;});
    Array.from(document.getElementsByClassName("title")).forEach((e) => {
        e.style.fontSize = space.mediumFontSize;
        e.style.color = space.purpleBackgroundDark;

    });

    /*
      By default the titles are all black which contrasts too much with the new
      colours so the following uses the same purple as the numbers to be a bit
      more gentle and increases the font size to make it easier to read.
    */
    Array.from(document.getElementsByClassName("titleline")).forEach((e) => {
        e.children[0].style.fontSize = space.mediumFontSize;
        e.children[0].style.color = space.purpleBackgroundDark;
    });

    /*
      To make it clearer which things are links, we want their background colour
      to change when hovered over.
     */
    document.styleSheets[0].insertRule('a:hover { background-color: ' + space.purpleBackgroundLight + ';}');

    document.getElementsByClassName("itemlist")[0].cellSpacing = 2;
    document.querySelectorAll(".subtext").forEach(el => el.remove());

    document.getElementsByTagName("tbody")[0].childNodes[0].remove();
    document.getElementsByClassName("morelink")[0].remove();
    document.getElementsByTagName("tbody")[0].childNodes[4].remove();

    Array.from(document.getElementsByTagName("a")).forEach((e) => {
        e.setAttribute("target", "_blank");
    });

    /*
      Remove indications that there is voting on this site to make it slightly
      less addictive.
     */
    Array.from(document.querySelectorAll('.itemlist > tbody > .athing')).forEach((e) => {
        e.children[1].remove();
    });

    var hnmain = document.getElementById("hnmain");
    hnmain.style.paddingTop = "50px";
    hnmain.style.background = space.lightLightYellow;
    hnmain.style.width = "55vw";

    Array.from(document.getElementsByClassName("spacer")).forEach((e) => {e.style.height = "10px";});
    document.getElementsByClassName("itemlist")[0].style.padding = "30px";

})();
