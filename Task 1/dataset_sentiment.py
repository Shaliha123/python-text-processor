import csv
import sqlite3
from datetime import datetime

# Simple sentiment function
def calculate_score(text):
    positive_words = ["good", "great", "excellent", "amazing", "love"]
    negative_words = ["bad", "worst", "poor", "hate"]

    score = 0
    text = text.lower()

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    return score

def get_sentiment(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# Connect to ONE database only
conn = sqlite3.connect("amazon_reviews.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS amazon_sentiment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_text TEXT,
    score INTEGER,
    sentiment TEXT,
    timestamp TEXT
)
""")

# Open CSV
try:
    with open("amazon.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            review_text = row["review_content"]

            score = calculate_score(review_text)
            sentiment = get_sentiment(score)
            print("Score:", score, "| Sentiment:", sentiment)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            INSERT INTO amazon_sentiment (review_text, score, sentiment, timestamp)
            VALUES (?, ?, ?, ?)
            """, (review_text, score, sentiment, timestamp))

    conn.commit()
    print("✅ All reviews processed and stored successfully!")

except FileNotFoundError:
    print("❌ CSV file not found. Check file name and location.")

# Show first 5 rows
cursor.execute("SELECT * FROM amazon_sentiment LIMIT 5")
rows = cursor.fetchall()

print("\nFirst 5 rows:\n")
for row in rows:
    print(row)

conn.close()