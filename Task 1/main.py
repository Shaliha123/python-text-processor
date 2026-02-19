import os
import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("reviews.db")

# Create cursor
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    score INTEGER,
    sentiment TEXT
)
""")

conn.commit()


# Positive and negative words
positive = ["good", "nice", "excellent", "happy"]
negative = ["bad", "terrible", "worst", "poor"]

# Get all text files from folder
files = os.listdir()

for file in files:
    if file.endswith(".txt"):   # only read txt files
        with open(file, "r") as f:
            text = f.read().lower()

        score = 0

        # Check positive words
        for word in positive:
            score += text.count(word)

        # Check negative words
        for word in negative:
            score -= text.count(word)

        print("File:", file)
        print("Score:", score)

        if score > 0:
            print("Positive Review ")
            sentiment = "Positive"
        elif score < 0:
            print("Negative Review ")
            sentiment = "Negative"
        else:
            print("Neutral Review ")
            sentiment = "Neural"
            cursor.execute(
    "INSERT INTO reviews (filename, score, sentiment) VALUES (?, ?, ?)",
    (file, score, sentiment)
)



            


conn.commit()

print("\n--- Data From Database ---")

cursor.execute("SELECT * FROM reviews")

rows = cursor.fetchall()

for row in rows:
    print(row)



print("--------------------")
