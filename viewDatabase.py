import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("instance/chessapp.sqlite")
gameHistory = con.execute(
    'SELECT * from history WHERE winner = ? OR loser = ? ORDER BY created', ("strandded", "strandded")
)
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
for game in gameHistory:
    print(type(game['created']))

con.close()