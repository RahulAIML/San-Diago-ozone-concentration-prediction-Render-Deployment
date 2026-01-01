import sqlite3
import pandas as pd
import os

db_path = 'database.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    try:
        query = "SELECT * FROM prediction_logs"
        table = pd.read_sql_query(query, conn)
        table.to_csv('predictionlog.csv', index=False)
        print("Exported predictionlog.csv")
    except Exception as e:
        print(f"Error exporting: {e}")
    finally:
        conn.close()
else:
    print(f"{db_path} not found.")
