import json
import os
import sqlite3


def extract_five_letter_words():
    # Ensure directory exists
    os.makedirs("es_data", exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect("es_data/es.db")
    cursor = conn.cursor()

    # Query 5-letter words from the database
    cursor.execute("SELECT word, en_translation FROM words WHERE LENGTH(word) = 5")
    words = cursor.fetchall()

    # Close database connection
    conn.close()

    if not words:
        print("No 5-letter words found")
        return

    # Create output format
    output_data = {
        "languageCode": "es",
        "wordGroups": [
            {
                "wordLength": 5,
                "words": [
                    {"word": word, "translation": translation}
                    for word, translation in words
                ],
            }
        ],
    }

    # Write to output file
    with open("es_data/words_es.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(
        f"Successfully extracted {len(output_data['wordGroups'][0]['words'])} five-letter words"
    )


if __name__ == "__main__":
    extract_five_letter_words()
