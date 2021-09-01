DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS chessboard;
DROP TABLE IF EXISTS history;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    elo INTEGER DEFAULT 1200
);

CREATE TABLE chessboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    white TEXT NOT NULL,
    black TEXT NOT NULL,
    fen TEXT NOT NULL
);
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_played TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    winner_id INTEGER NOT NULL,
    loser_id INTEGER NOT NULL,
    elo_change INTEGER NOT NULL,
    FOREIGN KEY (winner_id) REFERENCES user(id),
    FOREIGN KEY (loser_id) REFERENCES user(id)
);
