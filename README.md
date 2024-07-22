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
Sometimes, the CSVs you are working with may have a row correlation, meaning 

|    |        | 0        |        | random | #RIF!   |        |          | 0       | #RIF! | #RIF! |          |        | ____   |        | #RIF! | ....  | #RIF! | ///   |        |          | #RIF! | #RIF! | 0     | #RIF! | --    |        |          | ///// |        | ////// |        |        |        |        | #RIF! | /     |        |        |        | --    | #RIF! | ///   |
|----|--------|----------|--------|--------|---------|--------|----------|---------|-------|-------|----------|--------|--------|--------|-------|-------|-------|-------|--------|----------|-------|-------|-------|-------|-------|--------|----------|-------|--------|--------|--------|--------|--------|-------|-------|--------|--------|--------|-------|--------|--------|-------|
| 0  |        | #RIF!    |        | random | #RIF!   |        |          | 0       | #RIF! | #RIF! |          |        | ____   |        | #RIF! | ....  | #RIF! | ///   |        |          | #RIF! | #RIF! | 0     | #RIF! | --    |        |          | ///// |        | ////// |        |        |        |        | #RIF! | /     |        |        |        | --    | #RIF! | ///   |
| 1  |        |          | random | ..     | #RIF!   |        | /////////|         | #RIF! |       | #RIF!    | 0      | 0      | 0      | #RIF! |       | ..    | ----  | 0      | 0        |       |       | #RIF! | ..... | 0     | ...   |        | #RIF!  | .     |        |        | 0      |        |        |        | #RIF! | 0     |        | #RIF!  | 0      |        | 0      |        |        |
| 2  |        | caso     | #RIF!  | #RIF!  |         | 0      |          |         | 0     | 0     | _____    | _      |        |        |        | 0     | 0     | ///   | 0      |          | ____  | #RIF! | 0     |       | --    |        | 0        | #RIF!  | 0     | #RIF!  | 0      |        |        | ....   | ..    |        | -------|        | #RIF!  |        | 0      | #RIF!  | 0     |
| 3  |        | 0        | 0      | #RIF!  | 0       | ________| ........ | Tiziano   | Rossi | Verdi  | Marco  | Elena | VULGNE95E24B301X | M     | Vescovo | Caserta | 81031 | CE | 1997-03-24 | ///// | Via Verona | 5 | 80135 | Napoli | NA | VRSML97C24B301X | Eu 83.294,00 | Eu 68.537,00 | 0 | ........ | ____ | #RIF! | 0 | #RIF! | 0 | |        | |
| 4  |        | #RIF!    | 0      | 0      | _____   | --------|          | Campania | Napoli | Villa  | Giangiacomo | Luciana | VLLGC97C24B301W | 0      | Busto Garolfo | 0    | Milano | Lombardia | 20020 | MI | 1997-03-24 | ///// | Via Epomeo | 489 | 80126 | Napoli | VLLGC97C24B301W | Eu 83.294,00 | Eu 68.537,00 | 0 | ........ | ____ | #RIF! | 0 | #RIF! | 0 | |        | |
| 5  | ...    |          | 0      |        | ....    |        | -        | 0       | Lombardia | Bergamo | Ferrari  | Farhat | FHRFHT25C66H356T | 0      | Rivoli Veronese | #RIF! | Verona | Veneto | 37010 | VR | 1925-03-26 | ------ | Piazza Repubblica | 1 | 24050 | Zanica | BG | FHRFHT25C66H356T | Eu 4.771,00 | Eu 4.188,00 | 0 | ........ | ---- | ////// | 0 | 0 | . | #RIF! | 0 |
| 6  | #RIF!  |          |        |        |        | 0      | ////     | --------- | Campania | Napoli | Venturelli | Francesco | VNTRNC59R29F240C | M     | Mirandola | Modena | Emilia Romagna | 41037 | MO | 1959-10-29 | 0      | Via Monteoliveto | 1 | 80135 | Napoli | VNTRNC59R29F240C | Eu 84.020,00 | Eu 80.640,00 | #RIF! |         |        | 0      | ---  | 0      |        | __ |
| 7  | --     |          | ---------| 0 | #RIF! | ----   | 0        | Piemonte | Biella | Nocentini | Saadia | NCSDA33T48C112S | 0        | Castelfranco Di Sopra | #RIF! | Arezzo | Toscana | 52020 | AR | 1933-12-08 |        | Via Xxv Aprile | 15 | 13851 | Castelletto Cervo | BI | NCSDA33T48C112S | Eu 30.843,00 | Eu 21.587,00 | ...  | 0        | -------- | ....... |
| 8  | #RIF!  |          |        |        | 0      |        | #RIF!    | ---------| #RIF!  | Emilia Romagna | Ravenna | Bruno | Francesca | F      | Terranova Da Sibari | Taranto | Cosenza | Calabria | 87010 | CS | 1983-11-21 | Via Matteotti | 55 | 48010 | Cotignola | RA | BRNFNC83S61L124W | Eu 46.499,00 | Eu 36.566,00 | #RIF! | ______ | #RIF! | 0 | 0 | ------ | |
| 9  |        | 0        |        | #RIF!  | ////////| #RIF!  | 0        | Piemonte | Torino | Ricci | Mattia | RICMTT26M04I326A | M     | Sante Marie | L'Aquila | Abruzzo | 67067 | AQ | 1926-08-04 |        | Corso Re Umberto | 38 | 10128 | Torino | TO | RICMTT26M04I326A | Eu 80.583,00 | Eu 4.186,00 | 0 | #RIF! | #RIF! | ------ | 0 |
| 10 | 0      | #RIF!    |        | 0      |        | /      | #RIF!    | Lombardia | Milano | Caruso | Sara | CRSSRA70C65H922G | F     | ...   | San Giovanni La Punta | Catania | Sicilia | 95037 | CT | 1970-03-25 | 0      | Via Giambellino | 64 | 20146 | Milano | MI | CRSSRA70C65H922G | Eu 85.595,00 | Eu 78.088,00 | 0 | ------ | 0        |        | -------- | __ |
| 11 | 0      | #RIF!    |        | ----   | 0      | _      |          | #RIF!    | Emilia Romagna | Bologna | Piras | Sofia | PRSSFO91R59H766W | F     | San Basilio | Cagliari | Sardegna | 09040 | CA | 1991-10-19 | 0      | Via Appia | 24/B | 40026 | Imola | BO | PRSSFO91R59H766W | Eu 59.769,00 | Eu 13.577,00 |        | /////// | --     | ----- |
| 12 | 0      | -        |        | #RIF!  |        | #RIF!  | Abruzzo | Teramo | Valentini | Giovanni | VLNGNN70P11A202N | 0      | Cologna Spiaggia | 64020 | TE | 1970-11-24 | 0      | Via Mezzina | 53 | 64020 | Cologna Spiaggia | TE | VLNGNN70P11A202N | Eu 39.475,00 | Eu 13.796,00 | #RIF! | /////// | ////// |        | #RIF! |        | #RIF! |

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
| 4  |            |                              | Puglia                                    | Bari                         | Zanetti                      | 0          | -------- | ------                     |
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

### Case with only padding
Sometimes, the data entry clerk may start filling a table offsetted from the top-left corner, and export it with also
empty cells all around. We call such cells "padding". The CSV Trimmer can detect and remove them.

```python
from csv_trimming import CSVTrimmer

# Load your csv
csv = pd.read_csv("path/to/csv.csv")

# Instantiate the trimmer
trimmer = CSVTrimmer(drop_padding=True)

# And trim it
trimmed_csv = trimmer.trim(csv)
```

For instance, your input CSV to clean up may look like this at the beginning:

|   |   | region   | province       | surname |
|---|---|----------|----------------|---------|
| 0 |   |          |                |         |
| 1 |   |          |                |         |
| 2 |   | region   | province       | surname |
| 3 |   | Campania | Caserta        | Ferrero |
| 4 |   | Liguria  | Imperia        | Conti   |
| 5 |   | Puglia   | Bari           | Fabris  |
| 6 |   | Sardegna | Medio Campidano| Conti   |
| 7 |   | Lazio    | Roma           | Fabbri  |
| 8 |   |          |                |         |
| 9 |   |          |                |         |
| 10|   |          |                |         |
| 11|   |          |                |         |

And after the trimming, it will look like this:

|   | region   | province       | surname |
|---|----------|----------------|---------|
| 0 | Campania | Caserta        | Ferrero |
| 1 | Liguria  | Imperia        | Conti   |
| 2 | Puglia   | Bari           | Fabris  |
| 3 | Sardegna | Medio Campidano| Conti   |
| 4 | Lazio    | Roma           | Fabbri  |

## License
This package is released under MIT license.