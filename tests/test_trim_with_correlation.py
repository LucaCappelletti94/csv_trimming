import pandas as pd
from csv_trimming import CSVTrimmer
from italian_csv_type_prediction.simple_types.nan_type import NaNType


def correlation_callback(current_row: pd.DataFrame, next_row: pd.DataFrame) -> bool:
    for value in current_row:
        if value == "Piemonte":
            return True
    return False


def test_trim_with_correlation():
    csv = pd.read_csv("tests/test.csv", index_col=0)
    trimmer = CSVTrimmer(correlation_callback)
    result = trimmer.trim(csv)
    with open("tests/expected_result.csv", "r") as f:
        assert result.to_csv() == f.read()