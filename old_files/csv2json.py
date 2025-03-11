import csv
import argparse
import json

""" example of usage
python csv2json.py -in es.csv -out words_es.json -lang es
"""


def main():
    # Define command line arguments
    parser = argparse.ArgumentParser(description="Convert CSV to JSON.")
    parser.add_argument("-input", required=True, help="Input CSV file path")
    parser.add_argument("-lang", required=True, help="Lang code (2-letter)")
    parser.add_argument("-output", default="out.json", help="Output JSON")

    args = parser.parse_args()

    # Open input file
    with open(args.input, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader, None)

        # Map to store words grouped by length
        words_by_length = {}

        # Read all remaining records
        for record in reader:
            if len(record) >= 2:
                word = record[0].strip()
                translation = record[1].strip()
                word_length = len(word)  # Count Unicode characters
                if word_length not in words_by_length:
                    words_by_length[word_length] = []
                words_by_length[word_length].append(
                    {"word": word, "translation": translation}
                )

    # Create a new list with "wordLength" as key, sorted by wordLength
    word_groups = sorted(
        [
            {"wordLength": length, "words": words}
            for length, words in words_by_length.items()
        ],
        key=lambda x: x["wordLength"],
    )

    # Create final output with languageCode at top level
    output_data = {"languageCode": args.lang, "wordGroups": word_groups}

    # Create output JSON file
    with open(args.output, "w", encoding="utf-8") as jsonfile:
        json.dump(output_data, jsonfile, ensure_ascii=False, indent=4)

    print(f"Successfully converted text to JSON in {args.output}")


if __name__ == "__main__":
    main()
