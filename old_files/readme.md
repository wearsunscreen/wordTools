# WordTools

A suite of Python applications designed to create and manage a database of words for language learning and word games. The applications use SQLite to store words, their translations, and metadata about their sources. It supports multiple languages and allows for flexible querying and sorting of words based on various attributes.

## Summary

WordTools consists of three main tools:

1. `createWordDB.py` - Creates a new language database with tables for words, sources, and metadata
2. `addSources.py` - Adds source references to an existing language database from a CSV file
3. `addWords.py` - Adds words to the database from a CSV file, optionally linking them to sources

## Features

## Tools

### createWordDB.py

Creates a new SQLite database for a specific language with tables for words, sources, and metadata.

Usage:

```bash
python createWordDB.py <language_name> <english_name> <language_code>
```

Example:

```bash
python createWordDB.py "español" "Spanish" "es"
```

### addSources.py

Adds source references to an existing language database from a CSV file.

Usage:

```bash
python addSources.py <language_code> <csv_file>
```

The CSV file must contain these columns:

- `lang`: Language code matching the database
- `short_name`: 4-character source identifier
- `description`: Description of the source (max 120 chars)

Example:

```bash
python addSources.py es sources_es.csv
```

Example CSV content:

```csv
lang,short_name,description
es,WOKA,Wokabulary - https://wokabulary.com/wordlists/es/
es,ANCO,AnCora Spanish corpus
```

### addWords.py

Adds words to an existing language database from a CSV file, optionally linking them to sources.

## Database Schema

The database created by createWordDB.py contains the following tables:

### words

Stores individual words and their properties:

- `word_id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `word`: TEXT (required, unique, max 15 chars)
- `en_translation`: TEXT (required, max 120 chars)
- `level`: INTEGER (required, between 0-10)
- `isAnswer`: BOOLEAN (optional)
- `rootWord`: TEXT (optional, max 15 chars)
- `length`: INTEGER (required, between 1-15)

Indexes:

- `idx_length`: On length field for optimized sorting
- `idx_ans`: On isAnswer field for filtering

### sources

Stores information about word sources:

- `source_id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `short_name`: TEXT (required, unique, exactly 4 chars)
- `description`: TEXT (optional, max 120 chars)

### language_info

Stores metadata about the language:

- `language_name`: TEXT (required) - Name in native language
- `english_name`: TEXT (required) - Name in English
- `language_code`: TEXT (required) - ISO code (e.g., "es" for Spanish)

## Installation

Requirements:

- Python 3
- SQLite

Clone the repository:

```bash
git clone https://github.com/yourusername/wordtools.git
cd wordtools
```
