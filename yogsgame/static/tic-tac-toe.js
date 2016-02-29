var empty = "";
var cross = "X";
var nought = "O";
var player = cross;
var points = 0;
var squares = [];

var columns = [[0, 3, 6], [1, 4, 7], [2, 5, 8]];
var rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8]];
var diagonals = [[0, 4, 8], [2, 4, 6]];

function win(player) {
    return [columns, rows, diagonals].some(function(lines) {
        return lines.some(function(line) {
            return line.every(function(squareIndex) {
                return squares[squareIndex].firstChild.nodeValue === player;
            });
        });
    });
}

function submitScore(score) {
    var msg = {
        "messageType": "SCORE",
        "score": points
    };
    window.parent.postMessage(msg, "*");
}

// Sets height to width.
function resizeBoard() {
    var width = $('#tic-tac-toe td').width();
    $('#tic-tac-toe td').css({
        'height': width + 'px'
    });
    // Request the service to set the resolution of the
    // iframe correspondingly
    var boardSize = width*3 + 30; // We need some padding to make it fit
    var message =  {
        messageType: "SETTING",
        options: {
            "width": boardSize,
            "height": boardSize
        }
    };
    window.parent.postMessage(message, "*");
}

function startNewGame() {
    player = cross;
    moves = 0;
    for (var i = 0; i < squares.length; i += 1) {
        squares[i].firstChild.nodeValue = empty;
    }
}

function clickOnSquare() {
    // If already filled in.
    if (this.firstChild.nodeValue !== empty) {
        return;
    }

    // Perform the current player's move.
    this.firstChild.nodeValue = player;
    moves++;
    if (win(cross)) {
        console.log("Victory!");
        points++;
        startNewGame();
    } else if (moves === 9) {
        startNewGame();
    } else {
        noughtsTurn();
    }
}

function noughtsTurn() {
    while (true) {
        var randomIndex = Math.floor((Math.random()*9));
        var squareText = squares[randomIndex].firstChild;
        if (squareText.nodeValue === empty) {
            squareText.nodeValue = nought;
            moves++;
            if (win(nought)) {
                console.log("You have failed!");
                submitScore(points);
                points = 0;
                startNewGame();
            }
            return;
        }

    }
}

$(document).ready( function() {
    "use strict";

    window.addEventListener("message", function(evt) {
        if (evt.data.messageType === "ERROR") {
            alert(evt.data.info);
        } else {
            console.log("Tic-Tac-Toe: Unknown message type " + evt.data.messageType);
        }
    });

    var board = document.createElement("table");

    var index = 0;

    for (var i = 0; i < 3; i += 1) {
        var row = document.createElement("tr");
        board.appendChild(row);
        for (var j = 0; j < 3; j += 1) {
            var square = document.createElement("td");
            square.onclick = clickOnSquare;
            square.appendChild(document.createTextNode(empty));
            square.index = index++;
            row.appendChild(square);
            squares.push(square);
        }
    }

    $("#tic-tac-toe").html(board);

    startNewGame();
    resizeBoard();
});
