var socket = io.connect("http://" + document.domain + ":" + location.port);
var username = '';
var room = '';
var white_player = '';
var black_player = '';
var fen = '';


// Document Elements
const whiteUsernameBlock = document.getElementById('white-player');
const blackUsernameBlock = document.getElementById('black-player');
const gameOverText = document.getElementById('game-over');
const modal = document.getElementById("game-end-modal");
const modalSpan = document.getElementsByClassName("close")[0];

// chessboard
var board = null;
var game = new Chess();
var $status = $('#status');
var $fen = $('#fen');
var $pgn = $('#pgn');
var gameAlreadyEnded = false;
var winner = '';
var loser = '';
var config = {
draggable: true,
position: 'start',
onDrop: onDrop,
};
board = Chessboard('chessboard', config);
board.position();
updateStatus(false);

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
    // player trying to move out of turn
    if (game.turn() === 'b' && username != black_player){
        return 'snapback'
    }
    if ((game.turn() === 'w' && username != white_player)){
        return 'snapback'
    }
    var move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });
    // illegal move
    if (move === null) return 'snapback';
    
    var move_and_board = {
        move: move,
        board_state: game.fen()
    };

    socket.emit('chess move', move_and_board);
    board.position(game.fen());
    updateStatus(false);
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
    board.position(game.fen());
}

function updateStatus (update_from_server) {
    var status = '';
    var moveColor = 'White';
    if (game.turn() === 'b') {
        moveColor = 'Black';
        blackUsernameBlock.style.boxShadow = '0 0 2px 2px rgba(0, 0, 255, .9)';
        whiteUsernameBlock.style.boxShadow = '0 0 0px 0px rgba(0, 0, 255, .4)';
    }
    else {
        blackUsernameBlock.style.boxShadow = '0 0 0px 0px rgba(0, 0, 255, .4)';
        whiteUsernameBlock.style.boxShadow = '0 0 2px 2px rgba(0, 0, 255, .9)';
    }

    // checkmate
    if (game.in_checkmate()) {
        status = 'Game over, ' + moveColor + ' is in checkmate.';
        if (gameAlreadyEnded == false){
            gameAlreadyEnded = true;
            open_modal();
            gameOverText.innerHTML = status;
            winner = white_player;
            loser = black_player;
            blackUsernameBlock.style.boxShadow = '0 0 0px 0px rgba(0, 0, 255, .4)';
            whiteUsernameBlock.style.boxShadow = '0 0 0px 0px rgba(0, 0, 255, .9)';
            if (moveColor == 'White'){
                winner = black_player;
                loser = white_player;
                blackUsernameBlock.style.boxShadow = '0 0 4px 4px rgba(255, 255, 0, .5)';
            }
            else {
                whiteUsernameBlock.style.boxShadow = '0 0 4px 4px rgba(255, 255, 0, .5)';
            }
            console.log('game has ended!')
            var results = {
                winner: winner,
                loser: loser
            }
            // ensure that only a single call to the database is performed, preventing duplicate rows in history table
            if (update_from_server === false) socket.emit('game end', results);
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
async function fetch_username() {
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

async function fetch_fen() {
    return await fetch('/get_fen')
        .then(async function (response){
            return await response.json();
        })
        .then(function (text) {
            return text['board_position'];
        });
}

function set_color(color) {
    var player_and_color = {
        color: color,
        name: username
    };

    socket.emit('set color', player_and_color);
}

function open_modal() {
    modal.style.display = 'block';
}

modalSpan.onclick = function() {
    modal.style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }

socket.emit('set color', null);
socket.on('set player colors', function (player_colors) {
    white_player = player_colors['white'];
    black_player = player_colors['black'];
    document.getElementById('white-player').innerHTML = white_player;
    document.getElementById('black-player').innerHTML = black_player;
});

socket.on('reset board', function () {
    white_player = 'Empty';
    black_player = 'Empty';
});

socket.on('connect', async function() {
    username = await fetch_username();
    fen = await fetch_fen();
    game.load(fen);
    board.position(game.fen());
    if (username != ''){
        console.log(username + ' has joined the server!');
    }
});

socket.on("chess move", function(move) {
    game.move(move);
    board.position(game.fen());
    updateStatus(true);
});
