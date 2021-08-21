import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("instance/chessapp.sqlite")
df = pd.read_sql_query("SELECT * from user", con)

df2 = pd.read_sql_query("SELECT * from history", con)

df3 = pd.read_sql_query("SELECT * from chessboard", con)

# Verify that result of SQL query is stored in the dataframe
print(df.head())
print(df2.head())
print(df3.head())

con.close()