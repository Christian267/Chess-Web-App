var username = '';
var room = document.getElementById('room').innerHTML;
var roomNumber = room.charAt(room.length - 1);
var white_player = '';
var black_player = '';
var fen = '';
var socket = io.connect('http://' + document.domain + ':' + location.port);
// socket.join(room);

// Document Elements
const whiteUsernameBlock = document.getElementById('white-player');
const blackUsernameBlock = document.getElementById('black-player');
const gameOverText = document.getElementById('game-over');
const winnerName = document.getElementById('winner-name');
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
// updateStatus(false);

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
    // if (game.turn() === 'b' && username != black_player){
    //     return 'snapback'
    // }
    // if ((game.turn() === 'w' && username != white_player)){
    //     return 'snapback'
    // }
    var move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });
    // illegal move
    if (move === null) return 'snapback';
    
    var data = {
        move: move,
        board_state: game.fen(),
        roomType: 'practice_board',
        roomNumber: roomNumber
    };

    socket.emit('chess move', data);
    board.position(game.fen());
    updateStatus(false);
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
    board.position(game.fen());
}

function updateStatus (update_from_server) {
    var statusText = '';
    var moveColor = game.turn() === 'b' ? 'Black': 'White';
    highlight_current_turn();
    // checkmate
    if (game.in_checkmate()) {
        statusText = 'Game over, ' + moveColor + ' is in checkmate.';
        if (gameAlreadyEnded == false){
            gameAlreadyEnded = true;
            open_modal();
            gameOverText.innerHTML = statusText;
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
            winnerName.innerHTML = winner;
            console.log('game has ended!')
            const data = {
                roomType: 'chessboard',
                roomNumber: roomNumber,
                winner: winner,
                loser: loser
            }
            // ensure that only a single call to the database is performed, preventing duplicate rows in history table
            if (update_from_server === false) socket.emit('game end', data);
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
    return await fetch('/api/practiceboard/' + roomNumber.toString(), {
        method: "get",
    }).then(async function (response){
            return await response.json();
        })
        .then(function (text) {
            return text['fen'];
        });
}

async function fetch_puzzle() {
    return await fetch('api/chesspuzzle/', {
        method: "get",
    }).then(async function (response){
        return await response.json();
    })
    .then(function (puzzles) {
        return puzzles;
    })
}

function highlight_current_turn() {
    if (game.turn() === 'w') {
        blackUsernameBlock.style.boxShadow = '0 0 0px 0px rgba(0, 0, 255, 0)';
        whiteUsernameBlock.style.boxShadow = '0 0 2px 2px rgba(0, 0, 255, .9)';
    }
    else {
        blackUsernameBlock.style.boxShadow = '0 0 2px 2px rgba(0, 0, 255, .9)';
        whiteUsernameBlock.style.boxShadow = '0 0 0px 0px rgba(0, 0, 255, 0)';
    }
}

async function load_puzzle() {
    puzzles = await fetch_puzzle();
    const randInt = Math.floor(Math.random() * (Object.keys(puzzles).length) + 1).toString();
    puzzle = puzzles[randInt];
    const fen = {
        fen: puzzle['fen']
    }
    save_fen(fen);
    console.log(JSON.stringify(fen));
    socket.emit('practice board move')
}

function set_color(color) {
    socket.emit('set color', {
        'roomType': 'practice_board',
        'roomNumber': roomNumber,
        'color': color,
        'username': username
    });
}

function save_fen(fen) {
    fetch('api/practiceboard/' + roomNumber, {
        method: 'PUT',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(fen)
    })
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

// socket.emit('set color', {'roomType': 'practice_board', 'roomNumber': roomNumber});
socket.on('set player colors', function (player_colors) {
    white_player = player_colors['white'];
    black_player = player_colors['black'];
    if (white_player !== 'Empty')
        whiteUsernameBlock.innerHTML = white_player;
    else whiteUsernameBlock.innerHTML = 'Choose White';
    if (black_player !== 'Empty')
        blackUsernameBlock.innerHTML = black_player;
    else blackUsernameBlock.innerHTML = 'Choose Black';

});

socket.on("chess move", function(move) {
    game.move(move);
    board.position(game.fen());
    updateStatus(true);
});

socket.on('connect', async function() {
    username = await fetch_username();
    socket.emit('join room', { 'username': username, 'roomType': 'practice_board', 'roomNumber': roomNumber });
    fen = await fetch_fen();
    game.load(fen);
    board.position(game.fen());
    highlight_current_turn();
    
});

socket.on('disconnect', function() {
    console.log('disconnecting');
    socket.emit('leave room', { 'username': username, 'roomType': 'practice_board', 'roomNumber': roomNumber });
})

socket.on('join room announcement', function (data) {
    console.log("User \"" + data['username'] + '\" has joined ' + data['room'] + roomNumber );
});

socket.on('leave room announcement', function (data) {
    console.log('User \"' + data['username'] + '\" has left ' + data['room']);
});

socket.on('reset board', function () {
    white_player = 'Choose White';
    black_player = 'Choose Black';
});
