import sqlite3
import pandas as pd

db_path = 'd:/Ozone_Project_7th_dec/django_backend/db.sqlite3'
conn = sqlite3.connect(db_path)
query = "SELECT * FROM api_predictionlog"

table = pd.read_sql_query(query, conn)
table.to_csv('predictionlog.csv', index=False)

conn.close()
