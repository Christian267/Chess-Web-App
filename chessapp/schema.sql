DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS chessboard;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    pass VARCHAR NOT NULL,
    elo INT DEFAULT 1200
);

CREATE TABLE chessboard (
    id SERIAL PRIMARY KEY,
    white VARCHAR NOT NULL,
    black VARCHAR NOT NULL,
    fen VARCHAR NOT NULL
);
CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    time_played TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    winner_id INT NOT NULL,
    loser_id INT NOT NULL,
    elo_change INT NOT NULL,
    FOREIGN KEY (winner_id) REFERENCES users(id),
    FOREIGN KEY (loser_id) REFERENCES users(id)
);
