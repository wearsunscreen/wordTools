import sqlite3
import csv
import argparse
import sys


def display_sources(cursor):
    print("\nCurrent sources in database:")
    print("-" * 50)
    print(f"{'SHORT':6} | DESCRIPTION")
    print("-" * 50)

    cursor.execute("SELECT short_name, description FROM sources ORDER BY short_name")
    sources = cursor.fetchall()

    if not sources:
        print("No sources found in database")
    else:
        for short_name, description in sources:
            print(f"{short_name:6} | {description}")


def add_sources(language_code, csv_file):
    # Connect to the database
    db_file = f"word_{language_code}.db"

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Read the CSV file
        with open(csv_file, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            # Check if required columns exist
            required_columns = {"lang", "short_name", "description"}
            if not required_columns.issubset(csv_reader.fieldnames):
                print(
                    "Error: CSV file must contain 'lang', 'short_name', and 'description' columns"
                )
                sys.exit(1)

            sources_added = 0
            sources_skipped = 0

            # Process each row
            for row in csv_reader:
                # Skip if language doesn't match
                if row["lang"].strip().lower() != language_code.lower():
                    sources_skipped += 1
                    continue

                short_name = row["short_name"].strip()
                description = row["description"].strip()

                # Validate short_name length
                if len(short_name) != 4:
                    print(
                        f"Warning: Skipping source '{short_name}' - short_name must be exactly 4 characters"
                    )
                    sources_skipped += 1
                    continue

                # Validate description length
                if len(description) > 120:
                    print(
                        f"Warning: Skipping source '{short_name}' - description exceeds 120 characters"
                    )
                    sources_skipped += 1
                    continue

                try:
                    # Try to insert the source
                    cursor.execute(
                        """
                        INSERT INTO sources (short_name, description)
                        VALUES (?, ?)
                    """,
                        (short_name, description),
                    )
                    print(f"Added source: {short_name}")
                    sources_added += 1

                except sqlite3.IntegrityError:
                    # Source already exists
                    print(
                        f"Source '{short_name}' already exists in the database - skipping"
                    )
                    sources_skipped += 1

        # Commit the changes
        conn.commit()
        print(
            f"\nFinished processing sources. Added: {sources_added}, Skipped: {sources_skipped}"
        )

        # Display all sources in database
        display_sources(cursor)

    except sqlite3.OperationalError as e:
        print(
            f"Error: Could not open database '{db_file}'. Make sure the language database exists and is accessible."
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
        description="Add sources to a language database from a CSV file."
    )
    parser.add_argument(
        "language_code",
        type=str,
        help='The language code of the database (e.g., "es" for Spanish)',
    )
    parser.add_argument(
        "csv_file", type=str, help="Path to the CSV file containing sources data"
    )

    # Parse arguments
    args = parser.parse_args()

    # Add sources from the CSV file
    add_sources(args.language_code, args.csv_file)
