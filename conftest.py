"""Script to setup the test_readme.py file in the tests directory."""

import os
from pytest_readme import setup

setup()
os.rename("test_readme.py", "tests/test_readme.py")
