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
    return ("./problem-" + n + ".html");
}

updateStyle();

// Predicate for whether this is a page which presents the solution to one of
// the problems. This is used because we have slightly different setup required
// if it is a problem page vs the index or some other page.
function isProblemPage() {
    return (window.location.href.split("/").pop().includes("problem"));
}

// We add the links to the buttons after loading the page so that we can compute
// which problems to link to from the current URL.
function setUpPageLinks() {
    console.log("setting up page links");
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
}

// If it is a problem page then set up the links to the other problems.
isProblemPage() ? setUpPageLinks() : console.log("not setting up page links");
