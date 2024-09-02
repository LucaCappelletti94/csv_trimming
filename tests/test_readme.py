# # ✂️ CSV Trimming
# 
# [![PyPI](https://badge.fury.io/py/csv-trimming.svg)](https://badge.fury.io/py/csv-trimming)
# [![python](https://img.shields.io/pypi/pyversions/csv-trimming)](https://pypi.org/project/csv-trimming/)
# [![license](https://img.shields.io/pypi/l/csv-trimming)](https://pypi.org/project/csv-trimming/)
# [![Downloads](https://pepy.tech/badge/csv-trimming)](https://pepy.tech/projects/csv-trimming)
# [![Github Actions](https://github.com/LucaCappelletti94/csv_trimming/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/csv_trimming/actions/)
# [![Codacy Badge](https://app.codacy.com/project/badge/Grade/0968ff39b133475da3a9c528b8ae2c9d)](https://app.codacy.com/gh/LucaCappelletti94/csv_trimming/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
# 
# [CSV Trimming](https://github.com/LucaCappelletti94/csv_trimming) is a Python package designed to take messy CSVs — the kind you get from scraping websites, legacy systems, or poorly managed data — and transform them into clean, well-formatted CSVs with just one line of code. No need for complex setups or large language models. It’s simple, straightforward, and generally gets the job done.
# 
# ## How do I install this package?
# 
# As usual, just download it using pip:
# 
# ```shell
# pip install csv_trimming

# 
# ## How do I use this package?
# The package is very simple to use, just load your CSV and pass it to the trimmer.
# 
def test_line_22():
    import pandas as pd
    from csv_trimming import CSVTrimmer
    
    # Load your csv
    csv = pd.read_csv("tests/documents/noisy/sicilia.csv")
    # Instantiate the trimmer
    trimmer = CSVTrimmer()
    # And trim it
    trimmed_csv = trimmer.trim(csv)
    # That's it!

# 
# For instance, your input CSV to clean up may look like this at the beginning:
# 
# |   | 0   | 1                       | 2       | 3                                                | 4         |
# |---|-----|-------------------------|---------|--------------------------------------------------|-----------|
# | 0 | #RIF! | #RIF!                  | ......... | ///                                            | -----     |
# | 1 | ('surname',)('-',)(0,) | region                  | (""('surname',)('-',)(0,"),)(' ',)(1,)       | province  | surname   |
# | 2 | ------ | #RIF!                  | #RIF!    |                                                |           |
# | 3 | #RIF! | Calabria               | -------  | Catanzaro                                      | Rossi     |
# | 4 | 0     | Sicilia                | _____    | Ragusa                                         | Pinna     |
# | 5 | ""    | Lombardia              | ------   | Varese                                         | Sbrana    |
# | 6 | 0     | Lazio                  | __       | Roma                                           | Mair      |
# | 7 | _     | Sicilia                | #RIF!    | Messina                                        | Ferrari   |
# | 8 | ----- | ..                     | ""       | 0                                              | --------- |
# 
# And after the trimming, it will look like this:
# 
# |   | region    | province  | surname |
# |---|-----------|-----------|---------|
# | 0 | Calabria  | Catanzaro | Rossi   |
# | 1 | Sicilia   | Ragusa    | Pinna   |
# | 2 | Lombardia | Varese    | Sbrana  |
# | 3 | Lazio     | Roma      | Mair    |
# | 4 | Sicilia   | Messina   | Ferrari |
# 
# Magic!
# 
# ## Advanced trimming with row correlation
# Sometimes, the CSVs you are working with may have a row correlation, meaning part of a given row is inserted in the next row. Such cases are common when the data-entry clerk wants to make the whole table fit in their screen, and in order to do so, they split the row in two. While this is clearly an extremely bad practice, it happens in the real world and the CSV Trimmer can handle it with a little help.
# 
# You just need to provide a function that defines which rows are correlated, and the CSV Trimmer will take care of the rest. While in this example we are using a rather simple function and a relatively clean CSV, the package can handle more complex cases.
# 
def test_line_66():
    from typing import Tuple
    import pandas as pd
    from csv_trimming import CSVTrimmer
    
    def simple_correlation_callback(
        current_row: pd.Series,
        next_row: pd.Series
    ) -> Tuple[bool, pd.Series]:
        """Return the correlation between two rows.
        
        Parameters
        ----------
        current_row : pd.Series
            The current row being analyzed in the DataFrame.
        next_row : pd.Series
            The next row in the DataFrame.
    
        Returns
        -------
        Tuple[bool, pd.Series]
            A tuple with a boolean indicating if the rows are correlated
            and a Series with the merged row.
        """
    
        # All of the rows that have a subsequent correlated row are
        # non-empty, and the subsequent correlated rows are always
        # with the first cell empty.
        if pd.isna(next_row.iloc[0]) and all(pd.notna(current_row)):
            return True, pd.concat(
                [
                    current_row,
                    pd.Series({"surname": next_row.iloc[-1]}),
                ]
            )
    
        return False, current_row
    
    csv = pd.read_csv("tests/test.csv")
    trimmer = CSVTrimmer(simple_correlation_callback)
    result = trimmer.trim(csv)

# 
# In this case, our CSV looked like this at the beginning:
# 
# |    | region   | province        |
# |----|----------|-----------------|
# | 0  | Campania | Caserta          |
# | 1  |          | Ferrero          |
# | 2  | Liguria  | Imperia          |
# | 3  |          | Conti            |
# | 4  | Puglia   | Bari             |
# | 5  |          | Fabris           |
# | 6  | Sardegna | Medio Campidano  |
# | 7  |          | Conti            |
# | 8  | Lazio    | Roma             |
# | 9  |          | Fabbri           |
# 
# 
# And after the trimming, it will look like this:
# 
# |    | region   | province        | surname |
# |----|----------|-----------------|---------|
# | 0  | Campania | Caserta          | Ferrero |
# | 1  | Liguria  | Imperia          | Conti   |
# | 2  | Puglia   | Bari             | Fabris  |
# | 3  | Sardegna | Medio Campidano  | Conti   |
# | 4  | Lazio    | Roma             | Fabbri  |
# 
# ## More examples
# Here follow some examples of the package in action.
# 
# ### Case with duplicated schemas
# Sometimes, when chaining multiple CSVs in a poor manner, you may end up with duplicated schemas.
# The CSV Trimmer detects rows that match the detected header, and it can (optionally) remove them.
# 
def test_line_142():
    import pandas as pd
    from csv_trimming import CSVTrimmer
    
    # Load your csv
    csv = pd.read_csv("tests/documents/noisy/duplicated_schema.csv")
    # Instantiate the trimmer
    trimmer = CSVTrimmer()
    # And trim it
    trimmed_csv = trimmer.trim(csv, drop_duplicated_schema=True)
    # That's it!

# 
# For instance, your input CSV to clean up may look like this at the beginning:
# 
# |    | 0          | 1                            | 2      | 3                                         | 4                             | 5                             | 6          | 7        |
# |----|------------|------------------------------|--------|-------------------------------------------|------------------------------|------------------------------|------------|----------|
# | 0  | #RIF!      | ////                         | #RIF!  | #RIF!                                     | 0                             | ....                         | 0          | 0        |
# | 1  |            | ('surname',)('.',)(0,)       | region | province                                  | surname                      | ('province',)('_',)(1,)      |            | 0        |
# | 2  | 0          | ////////                     | region | province                                  | surname                      | 0                             | 0          |          |
# | 3  | _____      | ///////                      | region | province                                  | surname                      | #RIF!                        | #RIF!      |          |
# | 4  |            |                              | Puglia                                    | Bari                         | Zanetti                      | 0          | -------- |
# | 5  | 0          |                              | Piemonte| Alessandria                               | Fabbri                       |                              |            |          |
# | 6  | 0          | -------                      |        | #RIF!                                     | #RIF!                        | 0                            |            | ----     |
# | 7  | /////////  | /////////                    | Sicilia| Agrigento                                  | Ferretti                     | //////////                   |            | ----------|
# | 8  | __         | --------                     | Campania| Napoli                                    | Belotti                      |                              | ///        |          |
# | 9  |            | --------                     | 0      | /////                                      | ---                          | 0                            | /////      | ----------|
# | 10 | -----      | #RIF!                        | Liguria| Savona                                    | Casini                       | 0                            |            | #RIF!    |
# | 11 | ...        | 0                            |        | -----                                     |                              | --------                     | 0          | 0        |
# 
# And after the trimming, it will look like this:
# 
# |   | region   | province    | surname |
# |---|----------|-------------|---------|
# | 0 | Puglia   | Bari        | Zanetti |
# | 1 | Piemonte | Alessandria | Fabbri  |
# | 2 | Sicilia  | Agrigento   | Ferretti|
# | 3 | Campania | Napoli      | Belotti |
# | 4 | Liguria  | Savona      | Casini  |
# 
# ### Case with only padding
# Sometimes, the data entry clerk may start filling a table offsetted from the top-left corner, and export it with also
# empty cells all around. We call such cells "padding". The CSV Trimmer can detect and remove them.
# 
def test_line_186():
    import pandas as pd
    from csv_trimming import CSVTrimmer
    
    # Load your csv
    csv = pd.read_csv("tests/documents/noisy/padding.csv")
    
    # Instantiate the trimmer
    trimmer = CSVTrimmer()
    
    # And trim it
    trimmed_csv = trimmer.trim(csv, drop_padding=True)

# 
# For instance, your input CSV to clean up may look like this at the beginning:
# 
# |   |   | region   | province       | surname |
# |---|---|----------|----------------|---------|
# | 0 |   |          |                |         |
# | 1 |   |          |                |         |
# | 2 |   | region   | province       | surname |
# | 3 |   | Campania | Caserta        | Ferrero |
# | 4 |   | Liguria  | Imperia        | Conti   |
# | 5 |   | Puglia   | Bari           | Fabris  |
# | 6 |   | Sardegna | Medio Campidano| Conti   |
# | 7 |   | Lazio    | Roma           | Fabbri  |
# | 8 |   |          |                |         |
# | 9 |   |          |                |         |
# | 10|   |          |                |         |
# | 11|   |          |                |         |
# 
# And after the trimming, it will look like this:
# 
# |   | region   | province       | surname |
# |---|----------|----------------|---------|
# | 0 | Campania | Caserta        | Ferrero |
# | 1 | Liguria  | Imperia        | Conti   |
# | 2 | Puglia   | Bari           | Fabris  |
# | 3 | Sardegna | Medio Campidano| Conti   |
# | 4 | Lazio    | Roma           | Fabbri  |
# 
# 
# ## Command Line Interface
# The package also provides a command line interface to trim CSVs. It comes installed with the `setup.py` of the package, therefore after having pip installed the package, you can immediately use it from the command line.
# 
# You can use it by running the following command:
# 
# ```shell
# csv-trim tests/documents/noisy/sicilia.csv tests/documents/noisy/sicilia_trimmed.csv

# 
# It supports the following options to keep it from attempting some trimmings:
# 
# - `--keep-padding`: Do not attempt to remove padding.
# - `--keep-duplicated-schema`: Do not attempt to remove duplicated schemas.
# - `--no-restore-header`: Do not attempt to restore the header.
# 
# For instance:
#     
# ```shell
# csv-trim tests/documents/noisy/sicilia.csv tests/documents/noisy/sicilia_trimmed.csv --keep-padding

# 
# ## How do I contribute to this package?
# If you have identified some new corner case that the package does not handle, or you have a suggestion for a new feature, feel free to open an issue. If you want to contribute with code, open an issue describing the feature you intend to add and submit a pull request.
# 
# ## License
# This package is released under MIT license.