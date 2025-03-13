import csv
import sqlite3
from pathlib import Path


def import_words():
    # Get the absolute path to the CSV file and database
    current_dir = Path(__file__).parent
    csv_path = current_dir / "es_data/es_en_5.csv"
    db_path = current_dir / "es_data/es.db"

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the CSV file
    with open(csv_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        # Prepare the insert statement
        insert_stmt = """
        INSERT INTO words (word, en_translation, length, frequency, level, source)
        VALUES (?, ?, ?, 0, 0, 'ivan')
        """

        # Insert each row
        for row in csv_reader:
            try:
                cursor.execute(
                    insert_stmt, (row["word"], row["translation"], int(row["length"]))
                )
            except sqlite3.Error as e:
                print(f"Error inserting word '{row['word']}': {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Import completed successfully!")


if __name__ == "__main__":
    import_words()
