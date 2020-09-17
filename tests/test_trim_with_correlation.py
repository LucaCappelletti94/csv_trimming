from typing import Tuple
import pandas as pd
from csv_trimming import CSVTrimmer


def correlation_callback(current_row: pd.Series, next_row: pd.Series) -> Tuple[bool, pd.Series]:
    for value in current_row:
        if value == "Piemonte":
            return True, pd.concat([
                current_row,
                pd.Series({
                    "correlated_{}".format(key): value
                    for key, value in next_row.iteritems()
                })
            ])
    return False, current_row


def test_trim_with_correlation():
    csv = pd.read_csv("tests/test.csv", index_col=0)
    trimmer = CSVTrimmer(correlation_callback)
    result = trimmer.trim(csv)
    with open("tests/expected_result.csv", "r") as f:
        assert result.to_csv() == f.read()
