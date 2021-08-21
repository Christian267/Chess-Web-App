var socket = io.connect("http://" + document.domain + ":" + location.port);
var username = '';
var whitePlayer = '';
var blackPlayer = '';

// chessboard

var board = null;
var game = new Chess();
var $status = $('#status');
var $fen = $('#fen');
var $pgn = $('#pgn');
var gameAlreadyEnded = false
var winner = ''
var loser = ''

var config = {
draggable: true,
position: 'start',
onDrop: onDrop,
};
board = Chessboard('myBoard', config);
updateStatus();

function onDragStart (piece) {
// do not pick up pieces if the game is over
if (game.game_over()) return false;

// only pick up pieces for the side to move
if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
    (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
}
}

function onDrop (source, target) {
// see if the move is legal
var move = game.move({
    from: source,
    to: target,
    promotion: 'q'
});

// illegal move
if (move === null) return 'snapback';
else {
    socket.emit('chess move', move);
}
board.position(game.fen());
updateStatus();
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
board.position(game.fen());
}

function updateStatus () {
var status = '';

var moveColor = 'White';
if (game.turn() === 'b') {
    moveColor = 'Black';
}

// checkmate
if (game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
    if (gameAlreadyEnded == false){
        gameAlreadyEnded = true;
        document.getElementById('gameover').innerHTML = status;
        document.getElementById('winnerLabel').innerHTML = 'Winner:';

        if (moveColor == 'White'){
            winner = blackPlayer;
            loser = whitePlayer;
        }
        console.log('game has ended!')
        document.getElementById('winnerDiv').innerHTML = winner;
        var results = {
            winner: winner,
            loser: loser
        }
        socket.emit('game end', results);
    }

}

// draw
else if (game.in_draw()) {
    status = 'Game over, drawn position';
}

// game still on
else {
    status = moveColor + ' to move';

    // check?
    if (game.in_check()) {
    status += ', ' + moveColor + ' is in check';
    }
}
}

// Server communication

async function load_username() {
    return await fetch('/get_username')
        .then(async function (response){
            return await response.json();
        })
        .then(function (text) {
            return text['username'];
        });
}

async function load_players() {
    return await fetch('/get_players')
        .then(async function (response){
            return await response.json();
        })
        .then(function (text) {
            return text;
        });
}

function setColor(color){
    var playerAndColor = {
        color: color,
        name: username
    }

    socket.emit('set color', playerAndColor);
}

// function setBlack(){
//     var playerAndColor = {
//         color: 'black',
//         name: username
//     }

//     socket.emit('set color', playerAndColor);
// }

socket.on('set player colors', function (playerColors) {
    whitePlayer = playerColors['white'];
    blackPlayer = playerColors['black'];
    document.getElementById('whitePlayer').innerHTML = whitePlayer;
    document.getElementById('blackPlayer').innerHTML = blackPlayer;
});

socket.on('connect', async function() {
    username = await load_username();
    if (username != ''){
        console.log(username + ' has joined the server!');
        // players = load_players();
        // if (firstConnect == false){
        //     firstConnect == true
        //     whitePlayer = username
        // }   
        // else{
        //     if (secondConnect == false){
        //         secondConnect =
        //         BlackPlayer = username

        //     }
        // }
    }
});


socket.on("chess move", function(move) {
    game.move(move);
    board.position(game.fen());
    updateStatus();
});