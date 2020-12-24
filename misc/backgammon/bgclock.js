// This is used as a way to specify which key starts the timer for each player.
var PlayerKey = {
    PLAYERONE: 70,              // "f" key
    PLAYERTWO: 74               // "j" key
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
var playerOneTime = numMinutes * 60;
var playerTwoTime = numMinutes * 60;
var gameClockState = ClockState.OFF;


document.getElementById("playerOneTime").innerHTML = playerOneTime;
document.getElementById("playerTwoTime").innerHTML = playerTwoTime;


function runTimerOne() {
    playerOneTime--;
    document.getElementById("playerOneTime").innerHTML = playerOneTime;
    if (playerOneTime > 0) {
        if (gameClockState == ClockState.PLAYERONE) {
            var t = setTimeout(runTimerOne, 1000);
        }
    } else {
        clockRanOut(1);
    }
}

function runTimerTwo() {
    playerTwoTime--;
    document.getElementById("playerTwoTime").innerHTML = playerTwoTime;
    if (playerTwoTime > 0) {
        if (gameClockState == ClockState.PLAYERTWO) {
            var t = setTimeout(runTimerTwo, 1000);
        }
    } else {
        clockRanOut(2);
    }
}


function clockRanOut(playerNumber) {
    gameClockState = ClockState.OFF;
    var message = (playerNumber == 1 ? "Red" : "White") + " player ran out of time!";
    document.getElementById("result").innerHTML = message;
}


$('body').on('keyup', function() {
    if (event.which == PlayerKey.PLAYERONE) {
        document.getElementById("playerOneName").className = "playerOneOn"
        document.getElementById("playerOneTime").className = "playerOneOn"
        document.getElementById("playerTwoName").className = "playerTwoOff"
        document.getElementById("playerTwoTime").className = "playerTwoOff"
        if (gameClockState != ClockState.PLAYERONE) {
            gameClockState = ClockState.PLAYERONE;
            playerOneTime += numSecondsPerPlay;
     	      console.log("starting player one timer");
            runTimerOne();
        }
    } else if (event.which == PlayerKey.PLAYERTWO) {
        document.getElementById("playerOneName").className = "playerOneOff"
        document.getElementById("playerOneTime").className = "playerOneOff"
        document.getElementById("playerTwoName").className = "playerTwoOn"
        document.getElementById("playerTwoTime").className = "playerTwoOn"
        if (gameClockState != ClockState.PLAYERTWO) {
            gameClockState = ClockState.PLAYERTWO;
            playerTwoTime += numSecondsPerPlay;
            console.log("starting player two timer");
            runTimerTwo();
        }
    } else {
        console.log("neither f nor j so not doing anything...");
        console.log("the event code is " + event.which);
    }
});
