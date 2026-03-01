import sqlite3
import logging


# -------------------- CREATE CONNECTION --------------------
def create_connection():
    try:
        conn = sqlite3.connect("amazon_sentiment.db")
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return None


# -------------------- CREATE TABLE --------------------
def create_table(conn):
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amazon_sentiment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review TEXT,
                score INTEGER,
                sentiment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    except Exception as e:
        logging.error(f"Table creation error: {e}")


# -------------------- INSERT REVIEW --------------------
def insert_review(conn, review, score, sentiment):
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO amazon_sentiment (review, score, sentiment)
            VALUES (?, ?, ?)
        """, (review, score, sentiment))

        conn.commit()

    except Exception as e:
        logging.error(f"Insertion error: {e}")