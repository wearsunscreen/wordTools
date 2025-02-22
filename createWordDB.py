import sqlite3
import os
import argparse

# Example usage:
# python createWordDB.py español Spanish es


def create_database(language_name, english_name, language_code):
    # Define the file name for the database in the current directory
    db_file = f"word_{language_code}.db"
    db_path = db_file  # Save directly in the current directory

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the words table
    # Fields:
    # - word: TEXT, max 15 chars, required
    # - en_translation: TEXT, max 120 chars, required
    # - level: INTEGER, 0-10
    # - isAnswer: BOOLEAN
    # - rootWord: TEXT, max 15 chars
    # - length: INTEGER, 1-15
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS words (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL CHECK(LENGTH(word) <= 15),
            en_translation TEXT NOT NULL CHECK(LENGTH(en_translation) <= 120),
            level INTEGER CHECK(level BETWEEN 0 AND 10),
            isAnswer BOOLEAN,
            rootWord TEXT CHECK(LENGTH(rootWord) <= 15),
            length INTEGER CHECK(length > 0 AND length <= 15)
        )
    """
    )

    # Create the sources table
    # Fields:
    # - short_name: TEXT, 4 chars, required
    # - description: TEXT, max 120 chars
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_name TEXT NOT NULL CHECK(LENGTH(short_name) = 4),
            description TEXT CHECK(LENGTH(description) <= 120)
        )
    """
    )

    # Create the word_sources table to link words and sources
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS word_sources (
            word_id INTEGER,
            source_id INTEGER,
            FOREIGN KEY(word_id) REFERENCES words(word_id),
            FOREIGN KEY(source_id) REFERENCES sources(source_id),
            PRIMARY KEY (word_id, source_id)
        )
    """
    )

    # Create an index on the length field to optimize sorting and querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_length ON words(length)")

    # Create a shortened index on the isAnswer field to optimize filtering
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ans ON words(isAnswer)")

    # Create the language_info table to store metadata about the language
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS language_info (
            language_name TEXT NOT NULL,
            english_name TEXT NOT NULL,
            language_code TEXT NOT NULL
        )
    """
    )

    # Insert language metadata
    cursor.execute(
        """
        INSERT INTO language_info (language_name, english_name, language_code)
        VALUES (?, ?, ?)
    """,
        (language_name, english_name, language_code),
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Create a language database.")
    parser.add_argument(
        "language_name", type=str, help="The name of the language in its own language"
    )
    parser.add_argument(
        "english_name", type=str, help="The English name of the language"
    )
    parser.add_argument(
        "language_code", type=str, help='The language code (e.g., "es" for Spanish)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Create database with command-line arguments
    create_database(args.language_name, args.english_name, args.language_code)
    print("Database and tables created successfully.")
