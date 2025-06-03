import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect("sentiment_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            ticker TEXT,
            source TEXT,
            text TEXT,
            sentiment_score REAL,
            weighted_score REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_record(date, ticker, source, text, sentiment_score, weighted_score):
    conn = sqlite3.connect("sentiment_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO sentiment (date, ticker, source, text, sentiment_score, weighted_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, ticker, source, text, sentiment_score, weighted_score))
    conn.commit()
    conn.close()

def load_sentiment_history(ticker=None):
    conn = sqlite3.connect("sentiment_data.db")
    query = "SELECT * FROM sentiment"
    if ticker:
        query += " WHERE ticker = ?"
        df = pd.read_sql_query(query, conn, params=(ticker,))
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df
