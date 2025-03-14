import csv
import sqlite3
import os


def update_word_levels():
    # Database and CSV file paths
    db_path = os.path.join("es_data", "es.db")
    csv_path = os.path.join("es_data", "es_5_levels.csv")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read CSV and update levels
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        # Skip the header row
        next(csvreader)
        for row in csvreader:
            if len(row) == 2:
                word, level = row
                try:
                    # Update the level for the word
                    cursor.execute(
                        """
                        UPDATE words 
                        SET level = ? 
                        WHERE word = ?
                    """,
                        (int(level), word),
                    )
                except sqlite3.Error as e:
                    print(f"Error updating word '{word}': {e}")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Word levels updated successfully!")


if __name__ == "__main__":
    update_word_levels()
