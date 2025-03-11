# WordTools

A suite of Python applications designed to create and manage a database of words for language learning and word games. The applications use SQLite to store words, their translations, and metadata about their sources.

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

Usage:

```bash
python addWords.py <language_code> <csv_file>
```

The CSV file must contain these columns:

- `word`: The word to add (required, max 15 chars)
- `en_translation`: English translation (required, max 120 chars)
- `isAnswer`: "TRUE" or "FALSE" (required)
- `level`: Integer 0-9 (optional, defaults to 5)
- `source`: 4-character source identifier (optional)

Example:

```bash
python addWords.py es words.csv
```

Example CSV content:

```csv
word,en_translation,isAnswer,level,source
casa,house,TRUE,3,WOKA
perro,dog,FALSE,2,ANCO
```

## Database Schema

The database created by createWordDB.py contains the following tables:

### words

Stores individual words and their properties:

- `word_id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `word`: TEXT (required, unique, max 15 chars)
- `length`: INTEGER (required, normalized length of word, between 1-15)
- `en_translation`: TEXT (max 120 chars)
- `frequency`: REAL (number between 0 and 1.0 where 1.0 is most frequent)
- `level`: INTEGER (required, between 1-10, for level of difficulty, zero if unknown)
- `categories`: TEXT (comma separated list of word categories)
- `source': TEXT (required, short name of source of word)

Indexes:

- `idx_length`: On length field for optimized sorting
- `idx_level`: On isAnswer field for filtering
-

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
- SQLite - installed by default on python

Clone the repository:

```bash
git clone https://github.com/yourusername/wordtools.git
cd wordtools
```

To activate venv on Windows execute

```bash
.venv/Scripts/Activate
```
