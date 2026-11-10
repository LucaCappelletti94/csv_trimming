"""Test trimming of CSVs with empty edge columns."""

import io

import pandas as pd

from csv_trimming import CSVTrimmer


def test_trailing_empty_column():
    """A trailing all-empty column must be dropped, not crash the trimmer."""
    csv = pd.read_csv(io.StringIO("a,b,\n1,2,\n3,4,\n"))
    cleaned = CSVTrimmer().trim(csv, restore_header=False)
    assert cleaned.columns.tolist() == ["a", "b"]
    assert cleaned.values.tolist() == [[1, 2], [3, 4]]


def test_leading_empty_column():
    """A leading all-empty column must be dropped, not crash the trimmer."""
    csv = pd.read_csv(io.StringIO(",a,b\n,1,2\n,3,4\n"))
    cleaned = CSVTrimmer().trim(csv, restore_header=False)
    assert cleaned.columns.tolist() == ["a", "b"]
    assert cleaned.values.tolist() == [[1, 2], [3, 4]]
