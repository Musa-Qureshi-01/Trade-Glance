import sqlite3
import os

DB_FILE = "tradeglance.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def init_db():
    """
    Initializes the database table for user preferences or history (MVP).
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_search(ticker: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO user_searches (ticker) VALUES (?)", (ticker,))
    conn.commit()
    conn.close()
