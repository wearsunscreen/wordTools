# Project Name

wordTools

## Description

wordTools is a set of programs to convert input files of various source
to a JSON to be used by my word game.

## cvs2json

cvs2json is a program to convert CSV files to JSON. It expect the following columns:

```
spanish,english,Source
adiós,goodbye,Free Spanish Word Lists — Wokabulary
```

The program will output a JSON file with the following structure:

```
{
    "languageCode": "es",
    "wordGroups": [
        {
            "wordLength": 2,
            "words": [
                {
                    "word": "adiós",
                    "translation": "goodbye",
                    "source": "Free Spanish Word Lists — Wokabulary"
                }
            ]
        }
    ]
}
```
