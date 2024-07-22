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
