# WordTools

## Description

WordTools is a collection of Python applications designed to create and manage a database of words for language learning and word games. The applications use SQLite to store words, their translations, and metadata about their sources. It supports multiple languages and allows for flexible querying and sorting of words based on various attributes.

## Features

- Create a database for storing words and their translations.
- Support for multiple languages with metadata storage.
- Many-to-many relationship between words and their sources.
- Efficient querying and sorting with indexed fields.

## Installation

To use WordTools, ensure you have Python 3 and SQLite installed on your system. Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/yourusername/wordtools.git
cd wordtools
```

## Tools

### createWordDB

`createWordDB.py` is one of the tools in the WordTools collection. It allows you to create a new database for a specific language.

#### Usage

Run the `createWordDB.py` script with the required command-line arguments:

```bash
python createWordDB.py <language_name> <english_name> <language_code>
```

Example for Spanish:

```bash
python createWordDB.py español Spanish es
```

## Database Schema

The database consists of the following tables:

### `words`

- `word_id`: INTEGER, primary key, auto-incremented.
- `word`: TEXT, max 15 chars, required.
- `en_translation`: TEXT, max 120 chars, required.
- `level`: INTEGER, range 0-10.
- `isAnswer`: BOOLEAN.
- `rootWord`: TEXT, max 15 chars.
- `length`: INTEGER, range 1-15.

### `sources`

- `source_id`: INTEGER, primary key, auto-incremented.
- `short_name`: TEXT, exactly 4 chars, required.
- `description`: TEXT, max 120 chars.

### `word_sources`

- `word_id`: INTEGER, foreign key referencing `words(word_id)`.
- `source_id`: INTEGER, foreign key referencing `sources(source_id)`.
- Primary key: (`word_id`, `source_id`).

### `language_info`

- `language_name`: TEXT, name of the language in its own language.
- `english_name`: TEXT, English name of the language.
- `language_code`: TEXT, language code (e.g., "es" for Spanish).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
