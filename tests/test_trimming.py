from random_csv_generator import random_csv
from ugly_csv_generator import uglify
from csv_trimming import CSVTrimmer
from italian_csv_type_prediction.simple_types.nan_type import NaNType


def test_trim():
    csv = random_csv(10)
    ugly = uglify(csv, duplicate_schema=False, empty_rows=False, seed=29, )
    trimmer = CSVTrimmer()
    trimmed = trimmer.trim(ugly)