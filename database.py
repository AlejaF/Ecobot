import pandas as pd
import sqlite3

conn = sqlite3.connect("events.db")

df = pd.read_sql("SELECT * FROM eventos", conn)

df['hora'] = pd.to_datetime(df['timestamp']).dt.hour

print(df.groupby('hora').size())