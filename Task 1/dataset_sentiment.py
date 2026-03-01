import csv
import sqlite3
from datetime import datetime
from sentiment_logic import calculate_score, get_sentiment

def create_database():
    try:
        conn = sqlite3.connect("reviews.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS amazon_sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT,
            score INTEGER,
            sentiment TEXT,
            timestamp TEXT
        )
        """)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Database Error:", e)

def process_reviews():
    try:
        conn = sqlite3.connect("reviews.db")
        cursor = conn.cursor()

        with open("amazon.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                review_text = row["review_content"]

                score = calculate_score(review_text)
                sentiment = get_sentiment(score)
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                INSERT INTO amazon_sentiment (review, score, sentiment, timestamp)
                VALUES (?, ?, ?, ?)
                """, (review_text, score, sentiment, time_now))

        conn.commit()
        conn.close()

        print("✅ All reviews processed successfully!")

    except FileNotFoundError:
        print("❌ CSV file not found!")
    except sqlite3.Error as e:
        print("❌ Database Error:", e)

def show_summary():
    try:
        conn = sqlite3.connect("reviews.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM amazon_sentiment")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM amazon_sentiment WHERE sentiment='Positive'")
        positive = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM amazon_sentiment WHERE sentiment='Negative'")
        negative = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM amazon_sentiment WHERE sentiment='Neutral'")
        neutral = cursor.fetchone()[0]

        print("\n📊 Summary Statistics")
        print("Total Reviews:", total)
        print("Positive:", positive)
        print("Negative:", negative)
        print("Neutral:", neutral)

        conn.close()

    except sqlite3.Error as e:
        print("❌ Database Error:", e)

if __name__ == "__main__":
    create_database()
    process_reviews()
    show_summary()