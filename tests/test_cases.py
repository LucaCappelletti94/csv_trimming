"""Test cases from the documents collection."""

import os
from glob import glob
import pandas as pd
from tqdm.auto import tqdm
from csv_trimming import CSVTrimmer


def test_document_collection():
    """Test the document collection."""
    documents = glob("tests/documents/cleaned/*.csv")
    noisy_document_pattern = "tests/documents/noisy/{}"

    for document in tqdm(
        documents,
        desc="Testing documents",
        leave=False,
        dynamic_ncols=True,
    ):
        desinence = document.split(os.sep)[-1]
        noisy_document = noisy_document_pattern.format(desinence)

        noisy_csv = pd.read_csv(noisy_document, index_col=0)
        expected_cleaned_csv = pd.read_csv(document, index_col=0)

        trimmer = CSVTrimmer()
        trimmed_csv = trimmer.trim(noisy_csv)

        try:
            assert trimmed_csv.equals(expected_cleaned_csv)
        except AssertionError as exp:
            trimmed_csv.to_csv("tests/trimmed.csv", index=False)
            raise exp
    
    if os.path.exists("tests/trimmed.csv"):
        os.remove("tests/trimmed.csv")