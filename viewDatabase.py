import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("instance/chessapp.sqlite")
df = pd.read_sql_query("SELECT * from user", con)

df2 = pd.read_sql_query("SELECT * from history", con)

df3 = pd.read_sql_query("SELECT * from chessboard", con)

# Verify that result of SQL query is stored in the dataframe
print('TABLE: user')
print(df.head())
print('--------------------------------------------------')
print('TABLE: history')
print(df2.head())
print('--------------------------------------------------')
print('TABLE: chessboard')
print(df3.head())

con.close()