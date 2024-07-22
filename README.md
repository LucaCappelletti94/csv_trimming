# CSV Trimming

[![PyPI](https://badge.fury.io/py/csv-trimming.svg)](https://badge.fury.io/py/csv-trimming)
[![python](https://img.shields.io/pypi/pyversions/csv-trimming)](https://pypi.org/project/csv-trimming/)
[![license](https://img.shields.io/pypi/l/csv-trimming)](https://pypi.org/project/csv-trimming/)
[![Downloads](https://pepy.tech/badge/csv-trimming)](https://pepy.tech/projects/csv-trimming)
[![Github Actions](https://github.com/LucaCappelletti94/csv_trimming/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/csv_trimming/actions/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0968ff39b133475da3a9c528b8ae2c9d)](https://app.codacy.com/gh/LucaCappelletti94/csv_trimming/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Package python to remove common ugliness from real-world csv-like file.

When working with lots of CSVs from different companies or even worse

This package is to fix that kind of issues.

## How do I install this package?

As usual, just download it using pip:

```shell
pip install csv_trimming
```

## How do I use this package?
The package is very simple to use, just load your CSV and pass it to the trimmer.

```python
from csv_trimming import CSVTrimmer

# Load your csv
csv = pd.read_csv("path/to/csv.csv")
# Instantiate the trimmer
trimmer = CSVTrimmer()
# And trim it
trimmed_csv = trimmer.trim(csv)
# That's it!
```

For instance, your input CSV to clean up may look like this at the beginning:

|   | 0   | 1                       | 2       | 3                                                | 4         |
|---|-----|-------------------------|---------|--------------------------------------------------|-----------|
| 0 | #RIF! | #RIF!                  | ......... | ///                                            | -----     |
| 1 | ('surname',)('-',)(0,) | region                  | (""('surname',)('-',)(0,"),)(' ',)(1,)       | province  | surname   |
| 2 | ------ | #RIF!                  | #RIF!    |                                                |           |
| 3 | #RIF! | Calabria               | -------  | Catanzaro                                      | Rossi     |
| 4 | 0     | Sicilia                | _____    | Ragusa                                         | Pinna     |
| 5 | ""    | Lombardia              | ------   | Varese                                         | Sbrana    |
| 6 | 0     | Lazio                  | __       | Roma                                           | Mair      |
| 7 | _     | Sicilia                | #RIF!    | Messina                                        | Ferrari   |
| 8 | ----- | ..                     | ""       | 0                                              | --------- |

And after the trimming, it will look like this:

|   | region    | province  | surname |
|---|-----------|-----------|---------|
| 0 | Calabria  | Catanzaro | Rossi   |
| 1 | Sicilia   | Ragusa    | Pinna   |
| 2 | Lombardia | Varese    | Sbrana  |
| 3 | Lazio     | Roma      | Mair    |
| 4 | Sicilia   | Messina   | Ferrari |

Magic!

## Advanced trimming with row correlation






## More examples
Here follow some examples of the package in action.

### Case with duplicated schemas
Sometimes, when chaining multiple CSVs in a poor manner, you may end up with duplicated schemas.
The CSV Trimmer detects rows that match the detected header, and it can (optionally) remove them.

```python
from csv_trimming import CSVTrimmer

# Load your csv
csv = pd.read_csv("path/to/csv.csv")
# Instantiate the trimmer
trimmer = CSVTrimmer(drop_duplicated_schema=True)
# And trim it
trimmed_csv = trimmer.trim(csv)
# That's it!
```

For instance, your input CSV to clean up may look like this at the beginning:

|    | 0          | 1                            | 2      | 3                                         | 4                             | 5                             | 6          | 7        | 8                          |
|----|------------|------------------------------|--------|-------------------------------------------|------------------------------|------------------------------|------------|----------|----------------------------|
| 0  | #RIF!      | ////                         | #RIF!  | #RIF!                                     | 0                             | ....                         | 0          | 0        |                            |
| 1  |            | ('surname',)('.',)(0,)       | region | province                                  | surname                      | ('province',)('_',)(1,)      |            | 0        | ___                        |
| 2  | 0          | ////////                     | region | province                                  | surname                      | 0                             | 0          |          | ..........                 |
| 3  | _____      | ///////                      | region | province                                  | surname                      | #RIF!                        | #RIF!      |          | #RIF!                      |
| 4  |            |                              |        | Puglia                                    | Bari                         | Zanetti                      | 0          | -------- | ------                     |
| 5  | 0          |                              | Piemonte| Alessandria                               | Fabbri                       |                              |            |          |                            |
| 6  | 0          | -------                      |        | #RIF!                                     | #RIF!                        | 0                            |            | ----     |                            |
| 7  | /////////  | /////////                    | Sicilia| Agrigento                                  | Ferretti                     | //////////                   |            | ----------| #RIF!                     |
| 8  | __         | --------                     | Campania| Napoli                                    | Belotti                      |                              | ///        |                            |
| 9  |            | --------                     | 0      | /////                                      | ---                          | 0                            | /////      | ----------|                            |
| 10 | -----      | #RIF!                        | Liguria| Savona                                    | Casini                       | 0                            |            | #RIF!    | #RIF!                      |
| 11 | ...        | 0                            |        | -----                                     |                              | --------                     | 0          | 0        |                            |


And after the trimming, it will look like this:

|   | region   | province    | surname |
|---|----------|-------------|---------|
| 0 | Puglia   | Bari        | Zanetti |
| 1 | Piemonte | Alessandria | Fabbri  |
| 2 | Sicilia  | Agrigento   | Ferretti|
| 3 | Campania | Napoli      | Belotti |
| 4 | Liguria  | Savona      | Casini  |

## License
This package is released under MIT license.