import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("instance/chessapp.sqlite")
con.execute(
    '''INSERT INTO user (username, elo)
       VALUES (?, ?)''',
       ('Christian', 1100)
)
con.execute(
    '''INSERT INTO user (username, elo)
       VALUES (?, ?)''',
       ('chessmaster3000', 1400)
)
con.execute(
    '''INSERT INTO user (username, elo)
       VALUES (?, ?)''',
       ('strandded', 1200)
)

con.executemany(
    '''INSERT INTO history (winner_id, loser_id, elo_change)
       VALUES (?, ?, ?)''',
              [(2, 1, 23),
              (2, 1, 21),
              (2, 1, 20),
              (2, 1, 18),
              (2, 3, 25),
              (2, 3, 23),
              (3, 1, 23),
              (1, 3, 23)]
              )
con.commit()