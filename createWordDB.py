import os
import sqlite3
import sys


def create_database(db_path):
    """Create a new SQLite database with the required tables."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to database (this will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create language_info table
    cursor.execute(
        """
    CREATE TABLE language_info (
        language_name TEXT NOT NULL,
        english_name TEXT NOT NULL,
        language_code TEXT NOT NULL
    )
    """
    )

    # Create sources table
    cursor.execute(
        """
    CREATE TABLE sources (
        source_id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_name TEXT NOT NULL UNIQUE,
        description TEXT
        CHECK (length(short_name) = 4)
        CHECK (length(description) <= 120)
    )
    """
    )

    # Create words table
    cursor.execute(
        """
    CREATE TABLE words (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL UNIQUE,
        length INTEGER NOT NULL,
        en_translation TEXT,
        frequency REAL,
        level INTEGER NOT NULL,
        categories TEXT,
        source TEXT NOT NULL,
        CHECK (length(word) <= 15)
        CHECK (length >= 1 AND length <= 15)
        CHECK (length(en_translation) <= 120)
        CHECK (frequency >= 0 AND frequency <= 1.0)
        CHECK (level >= 0 AND level <= 10)
        FOREIGN KEY (source) REFERENCES sources(short_name)
    )
    """
    )

    # Create indexes
    cursor.execute("CREATE INDEX idx_length ON words(length)")
    cursor.execute("CREATE INDEX idx_level ON words(level)")

    # Insert Spanish language info
    cursor.execute(
        """
    INSERT INTO language_info (language_name, english_name, language_code)
    VALUES (?, ?, ?)
    """,
        ("español", "Spanish", "es"),
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()


def main():
    # Define database path and ensure parent directory exists
    db_dir = "es_data"
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "es.db")

    # Check if database already exists
    if os.path.exists(db_path):
        print(f"Error: Database already exists at {db_path}")
        sys.exit(1)

    try:
        create_database(db_path)
        print(f"Successfully created database at {db_path}")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
