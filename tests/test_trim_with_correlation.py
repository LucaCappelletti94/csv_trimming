"""Test the trim method with correlation."""

from typing import Tuple
import pandas as pd
from csv_trimming import CSVTrimmer


def correlation_callback(
    current_row: pd.Series, next_row: pd.Series
) -> Tuple[bool, pd.Series]:
    """Return the correlation between two rows.

    Parameters
    --------------------------
    current_row: pd.Series,
        The current row.
    next_row: pd.Series,
        The next row.
    """
    for value in current_row:
        if value == "Piemonte":
            return True, pd.concat(
                [
                    current_row,
                    pd.Series(
                        {f"correlated_{key}": value for key, value in next_row.items()}
                    ),
                ]
            )
    return False, current_row


def test_trim_with_correlation():
    """Test the trim method with correlation."""
    csv = pd.read_csv("tests/test.csv", index_col=0)
    trimmer = CSVTrimmer(correlation_callback)
    result = trimmer.trim(csv)
    with open("tests/expected_result.csv", "r", encoding="utf8") as f:
        assert result.to_csv() == f.read()


def simple_correlation_callback(
    current_row: pd.Series, next_row: pd.Series
) -> Tuple[bool, pd.Series]:
    """Return the correlation between two rows."""

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


def test_trim_correlation_simple():
    """Test the trim method with correlation."""
    csv = pd.read_csv("tests/trim_correlation_simple.csv", index_col=0, header=None)
    expected = pd.read_csv("tests/trim_correlation_simple_cleaned.csv", index_col=0)
    trimmer = CSVTrimmer(simple_correlation_callback)
    result = trimmer.trim(csv)
    assert result.equals(expected)
