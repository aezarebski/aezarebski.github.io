// This is used as a way to specify which key starts the timer for each player.
var PlayerKey = {
    PLAYERONE: 114,
    PLAYERTWO: 119
};
// This is used to specify which player's clock is currently running.
var ClockState = {
    OFF: 0,
    PLAYERONE: 1,
    PLAYERTWO: 2
};
// The number of minutes allocated to each player at the start of the match.
var numMinutes = 3;
// The number of seconds that each player gets to make a move.
var numSecondsPerPlay = 15;
var playerOneTime;
var playerTwoTime;
var gameClockState = ClockState.OFF;
function restartClock() {
    console.log("setting the clocks to initial state");
    document.getElementById("playerOneName").className = "playerOneOff";
    document.getElementById("playerOneTime").className = "playerOneOff";
    document.getElementById("playerOneBox").className = "playerOneBoxOff";
    document.getElementById("playerTwoName").className = "playerTwoOff";
    document.getElementById("playerTwoTime").className = "playerTwoOff";
    document.getElementById("playerTwoBox").className = "playerTwoBoxOff";
    playerOneTime = numMinutes * 60;
    playerTwoTime = numMinutes * 60;
    gameClockState = ClockState.OFF;
    document.getElementById("playerOneTime").innerHTML = playerOneTime.toString();
    document.getElementById("playerTwoTime").innerHTML = playerTwoTime.toString();
}
function refreshClockOne() {
    document.getElementById("playerOneTime").innerHTML = playerOneTime.toString();
}
function refreshClockTwo() {
    document.getElementById("playerTwoTime").innerHTML = playerTwoTime.toString();
}
function runTimerOne() {
    if (gameClockState == ClockState.PLAYERONE) {
        playerOneTime--;
        refreshClockOne();
        if (playerOneTime > 0) {
            var t = setTimeout(runTimerOne, 1000);
        }
        else {
            clockRanOut(1);
        }
    }
}
function runTimerTwo() {
    if (gameClockState == ClockState.PLAYERTWO) {
        playerTwoTime--;
        refreshClockTwo();
        if (playerTwoTime > 0) {
            var t = setTimeout(runTimerTwo, 1000);
        }
        else {
            clockRanOut(2);
        }
    }
}
function clockRanOut(playerNumber) {
    gameClockState = ClockState.OFF;
    var message = (playerNumber == 1 ? "Red" : "White") + " player ran out of time!";
    document.getElementById("result").innerHTML = message;
}
function startOne() {
    if (gameClockState == ClockState.PLAYERTWO) {
        playerTwoTime += numSecondsPerPlay;
        refreshClockTwo();
    }
    document.getElementById("playerOneName").className = "playerOneOn";
    document.getElementById("playerOneTime").className = "playerOneOn";
    document.getElementById("playerOneBox").className = "playerOneBoxOn";
    document.getElementById("playerTwoName").className = "playerTwoOff";
    document.getElementById("playerTwoTime").className = "playerTwoOff";
    document.getElementById("playerTwoBox").className = "playerTwoBoxOff";
    if (gameClockState != ClockState.PLAYERONE) {
        gameClockState = ClockState.PLAYERONE;
        console.log("starting player one timer");
        runTimerOne();
    }
}
function startTwo() {
    if (gameClockState == ClockState.PLAYERONE) {
        playerOneTime += numSecondsPerPlay;
        refreshClockOne();
    }
    document.getElementById("playerOneName").className = "playerOneOff";
    document.getElementById("playerOneTime").className = "playerOneOff";
    document.getElementById("playerOneBox").className = "playerOneBoxOff";
    document.getElementById("playerTwoName").className = "playerTwoOn";
    document.getElementById("playerTwoTime").className = "playerTwoOn";
    document.getElementById("playerTwoBox").className = "playerTwoBoxOn";
    if (gameClockState != ClockState.PLAYERTWO) {
        gameClockState = ClockState.PLAYERTWO;
        console.log("starting player two timer");
        runTimerTwo();
    }
}
function respondToEvent() {
    if (event.which == PlayerKey.PLAYERONE) {
        startOne();
    }
    else if (event.which == PlayerKey.PLAYERTWO) {
        startTwo();
    }
    else {
        console.log("neither w nor r so not doing anything...");
        console.log("the event code is " + event.which);
    }
}
;
restartClock();
