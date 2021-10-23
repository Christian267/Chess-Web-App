DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS chessboard;
DROP TABLE IF EXISTS practice_board;
DROP TABLE IF EXISTS chess_puzzles;

CREATE TABLE users (
    id       SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    pw       VARCHAR NOT NULL,
    elo      INT NOT NULL DEFAULT 1200
);

CREATE TABLE chessboard (
    id              SERIAL PRIMARY KEY,
    black           VARCHAR NOT NULL DEFAULT 'Empty',
    white           VARCHAR NOT NULL DEFAULT 'Empty',
    board_status    VARCHAR NOT NULL DEFAULT 'Available',
    user_count      INT NOT NULL DEFAULT 0,
    turn_number     INT NOT NULL DEFAULT 0,
    fen             VARCHAR NOT NULL DEFAULT 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
);

CREATE TABLE practice_board (
    id              SERIAL PRIMARY KEY,
    board_status    VARCHAR NOT NULL DEFAULT 'Available',
    user_count      INT NOT NULL DEFAULT 0,
    fen             VARCHAR NOT NULL DEFAULT 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
);

CREATE TABLE chess_puzzle (
    id          SERIAL PRIMARY KEY,
    fen         VARCHAR NOT NULL,
    solution    VARCHAR NOT NULL
);

CREATE TABLE history (
    id          SERIAL PRIMARY KEY,
    time_played TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    winner_id   INT NOT NULL,
    loser_id    INT NOT NULL,
    elo_change  INT NOT NULL,
    game_length INT NOT NULL,
    FOREIGN KEY (winner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (loser_id) REFERENCES users(id) ON DELETE CASCADE
);
