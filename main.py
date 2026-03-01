
import logging
import time
import csv
import pandas as pd
from tabulate import tabulate

from sentiment.analyzer import calculate_score, assign_sentiment
from database.db import create_connection, create_table, insert_review


# -------------------- LOGGING SETUP --------------------
logging.basicConfig(
    filename="process.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

start_time = time.time()


# -------------------- PROCESS REVIEWS --------------------
def process_reviews():
    try:
        conn = create_connection()
        if conn is None:
            return

        create_table(conn)

        with open("data/amazon.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            total = 0
            positive = 0
            negative = 0
            neutral = 0

            for row in reader:
                review_text = row.get("review_content")

                if not review_text:
                    continue

                score = calculate_score(review_text)
                sentiment = assign_sentiment(score)

                insert_review(conn, review_text, score, sentiment)

                total += 1

                if sentiment == "Positive":
                    positive += 1
                elif sentiment == "Negative":
                    negative += 1
                else:
                    neutral += 1

                # Log every 1000 rows (for large data handling)
                if total % 1000 == 0:
                    logging.info(f"Processed {total} rows")

            print("\n===== PROCESSING COMPLETE =====")
            print("Total Reviews:", total)
            print("Positive:", positive)
            print("Negative:", negative)
            print("Neutral:", neutral)

            logging.info(f"Finished processing {total} reviews")

        conn.close()

    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print("Unexpected error:", e)
        logging.error(str(e))


# -------------------- DISPLAY SUMMARY --------------------
def show_overall_summary():
    conn = create_connection()
    if conn is None:
        return

    try:
        df = pd.read_sql_query(
            "SELECT score, sentiment FROM amazon_sentiment",
            conn
        )

        print("\n===== OVERALL SUMMARY =====")
        print("Total Reviews:", len(df))

        print("\nSentiment Count:")
        print(df["sentiment"].value_counts())

        print("\nScore Statistics:")
        print(df["score"].describe())

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()


# -------------------- DISPLAY TABLE --------------------
def display_summary_table():
    conn = create_connection()
    if conn is None:
        return

    try:
        query = """
            SELECT score, sentiment
            FROM amazon_sentiment
            LIMIT 50
        """

        df = pd.read_sql_query(query, conn)

        print("\n===== SENTIMENT TABLE (First 50 Reviews) =====\n")
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=True))

    except Exception as e:
        print("Error fetching data:", e)

    finally:
        conn.close()


# -------------------- MAIN --------------------
if __name__ == "__main__":
    process_reviews()
    show_overall_summary()
    display_summary_table()

    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    print("\nExecution Time:", execution_time, "seconds")
    logging.info(f"Execution completed in {execution_time} seconds")