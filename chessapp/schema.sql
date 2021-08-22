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
    black TEXT NOT NULL
);
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    winner TEXT NOT NULL,
    loser TEXT NOT NULL,
    winnerElo INTEGER,
    loserElo INTEGER,
    eloChange INTEGER,
    FOREIGN KEY (winner) REFERENCES user (id),
    FOREIGN KEY (loser) REFERENCES user (id)
);
