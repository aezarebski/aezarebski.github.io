var defaultStyle = "dark";
const validStyleNames = ["light", "dark"];


function setStyleSheet(url) {
    console.log("Setting the stylesheet variable to " + url);
    var stylesheet = document.getElementById("stylesheet");
    stylesheet.setAttribute('href', url);
    return (null);
}

function setStylePreference(preference) {
    localStorage.setItem("style", validStyleNames.includes(preference) ? preference : defaultStyle);
    return (null);
}

function getStylePreference() {
    return ((!localStorage.getItem("style")) ? defaultStyle : localStorage.getItem("style"));
}

function toggleStyle() {
    var currPreference = getStylePreference();
    if (currPreference == "dark") {
        setStylePreference("light");
    } else {
        setStylePreference("dark");
    }
    updateStyle();
    return (null);
}

function updateStyle() {
    var preference = getStylePreference();
    var styleUrl = (preference == "light") ? "../../css/stylesheet.css" : "../../css/stylesheet-dark.css";
    setStyleSheet(styleUrl);
    return (null);
}

function problemFile(n) {
    return("./problem-" + n + ".html");
}

updateStyle();

// We add the links to the buttons after loading the page so that we can compute
// which problems to link to from the current URL.
var problemNumber = window
    .location
    .href
    .split("/")
    .pop()
    .match(/[0-9]+/)
    .toString();
document
    .getElementById("prevProblem")
    .setAttribute("href", problemFile(Number(problemNumber) - 1));
document
    .getElementById("nextProblem")
    .setAttribute("href", problemFile(Number(problemNumber) + 1));
