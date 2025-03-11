import sqlite3
import csv
import argparse
import sys


# add words from CSV file to words table
def add_words(language_code, csv_file):
    # Connect to the database
    db_file = f"word_{language_code}.db"

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Read the CSV file
        with open(csv_file, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            # Check if required columns exist
            required_columns = {"word", "en_translation", "isAnswer"}
            if not required_columns.issubset(csv_reader.fieldnames):
                print(
                    "Error: CSV file must contain 'word', 'en_translation', and 'isAnswer' columns"
                )
                sys.exit(1)

            words_added = 0
            words_skipped = 0
            sources_linked = 0

            # Process each row
            for row in csv_reader:
                word = row["word"].strip()
                en_translation = row["en_translation"].strip()
                isAnswer = row["isAnswer"].strip()
                source = row.get("source", "").strip()  # Get source if present

                # if length field is not present, set it to 5
                if "level" not in row:
                    level = "5"
                else:
                    level = row["level"].strip()

                # Validate word length
                if len(word) > 15:
                    print(
                        f"Warning: Skipping word '{word}' - word exceeds 15 characters"
                    )
                    words_skipped += 1
                    continue

                # Validate level, if integer value is not between 1 and 6, set it to 5
                if int(level) not in range(0, 10):
                    print(f"Warning: Skipping word '{word}' - invalid level")
                    words_skipped += 1
                    continue

                # Validate isAnswer
                if isAnswer not in ["TRUE", "FALSE"]:
                    print(f"Warning: Skipping word '{word}' - invalid isAnswer")
                    words_skipped += 1
                    continue

                try:
                    # Try to insert the word
                    cursor.execute(
                        """
                        INSERT INTO words (word, en_translation, level, isAnswer, length)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (word, en_translation, level, isAnswer, len(word)),
                    )
                    word_id = cursor.lastrowid
                    print(f"Added word: {word}")
                    words_added += 1

                    # If source is provided, link it
                    if source:
                        try:
                            # Get source_id
                            cursor.execute(
                                "SELECT source_id FROM sources WHERE short_name = ?",
                                (source,),
                            )
                            result = cursor.fetchone()
                            if result:
                                source_id = result[0]
                                cursor.execute(
                                    """
                                    INSERT INTO word_sources (word_id, source_id)
                                    VALUES (?, ?)
                                """,
                                    (word_id, source_id),
                                )
                                sources_linked += 1
                        except sqlite3.IntegrityError:
                            print(
                                f"Warning: Word-source link already exists for '{word}'"
                            )
                        except sqlite3.Error as e:
                            print(f"Error linking source for word '{word}': {e}")

                except sqlite3.IntegrityError:
                    # Word already exists
                    print(
                        f"Warning: Skipping word '{word}' - already exists in the database"
                    )
                    words_skipped += 1

        # Commit the changes
        conn.commit()
        print(
            f"\nFinished processing words. Added: {words_added}, Skipped: {words_skipped}, Sources linked: {sources_linked}"
        )

    except sqlite3.OperationalError as e:
        print(
            f"Error: Could not open database '{db_file}'. Make sure the language database exists."
        )
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Could not find CSV file '{csv_file}'")
        sys.exit(1)
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Add words to a language database from a CSV file."
    )
    parser.add_argument(
        "language_code",
        type=str,
        help='The language code of the database (e.g., "es" for Spanish)',
    )
    parser.add_argument(
        "csv_file", type=str, help="Path to the CSV file containing word data"
    )

    # Parse arguments
    args = parser.parse_args()

    # Add words from the CSV file
    add_words(args.language_code, args.csv_file)
