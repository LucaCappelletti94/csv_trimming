"""Test the CSVTrimmer class."""

import random
from random_csv_generator import random_csv
from ugly_csv_generator import uglify
from tqdm.auto import trange
from csv_trimming import CSVTrimmer


def test_trim():
    """Test the trim method."""
    state = random.Random(1234)
    for iteration in trange(100):
        csv = random_csv(
            number_of_rows=state.randint(1, 100),
            random_state=(iteration + 1) * 543678,
            localization="en_US.UTF-8",
        )
        ugly = uglify(
            csv,
            duplicate_schema=False,
            seed=(iteration + 1) * 5443678,
        )
        trimmer = CSVTrimmer()
        trimmer.trim(ugly)
