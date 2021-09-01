import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("instance/chessapp.sqlite")
gameHistory = pd.read_sql_query(
     '''SELECT winner.username      AS winner_username,
               loser.username       AS loser_username,
               winner.elo           AS winner_elo,
               loser.elo            AS loser_elo,
               history.elo_change   AS elo_change,
               history.time_played  AS time_played
        FROM   history 
            INNER JOIN user AS winner
                ON history.winner_id=winner.id
            INNER JOIN user AS loser
                ON history.loser_id=loser.id
        WHERE winner.id=1
            OR loser.id=1''',
        con)
userTable = pd.read_sql_query("SELECT * from user", con)

historyTable = pd.read_sql_query("SELECT * from history", con)

chessboardTable = pd.read_sql_query("SELECT * from chessboard", con)

# Verify that result of SQL query is stored in the dataframe
print('TABLE: user')
print(userTable)
print('--------------------------------------------------')
print('TABLE: history')
print(historyTable)
print('--------------------------------------------------')
print('TABLE: chessboard')
print(chessboardTable)
print('--------------------------------------------------')
print('QUERY: history INNER JOIN user')
print(gameHistory)
con.close()