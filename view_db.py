import sqlite3
import pandas as pd
import os

DB_PATH = 'database.db'

def view_logs():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        # Check if table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prediction_logs';")
        if not cursor.fetchone():
            print("Table 'prediction_logs' does not exist yet.")
            return

        query = "SELECT * FROM prediction_logs ORDER BY created_at DESC LIMIT 15"
        df = pd.read_sql_query(query, conn)
        
        print(f"\n--- Last 15 Predictions from {DB_PATH} ---\n")
        
        if df.empty:
            print("No logs found.")
            return

        for index, row in df.iterrows():
            print(f"ID: {row['id']}")
            print(f"Time: {row['created_at']}")
            print(f"Input: {row['input_data'][:100]}...") # Truncate
            print(f"Output: {row['predicted_output']}")
            print("-" * 50)
            
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    view_logs()
