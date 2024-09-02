"""Test suite to verify that the CLI of the package works as expected.

The CLI commands are of the form:

```bash
csv-trim input.csv output.csv
```

where `input.csv` is the path to the input CSV file and `output.csv` is the path to save the cleaned CSV file.

The CLI also supports the following options:

- `--restore-header`: Attempts to restore the header.
- `--drop-padding`: Attempts to drop padding.
- `--drop-duplicated-schema`: Attempts to drop duplicated schema.

The tests in this module verify that the CLI commands work as expected.
"""
import os
import subprocess
import pandas as pd
from csv_trimming import CSVTrimmer

def test_cli():
    """Test that the CLI works as expected."""

    paths = [
        "tests/test.csv",
        "tests/documents/noisy/padding.csv",
        "tests/documents/noisy/duplicated_schema.csv",
        "tests/documents/noisy/sicilia.csv",
    ]

    for path in paths:
        for restore_header in (True, False):
            for drop_padding in (True, False):
                for drop_duplicated_schema in (True, False):
                    trimmer = CSVTrimmer()
                    csv = pd.read_csv(path)
                    cleaned_csv = trimmer.trim(
                        csv,
                        restore_header=restore_header,
                        drop_padding=drop_padding,
                        drop_duplicated_schema=drop_duplicated_schema,
                    )

                    # We store the cleaned CSV in a temporary file
                    cleaned_csv.to_csv("tests/output.tmp.csv", index=False)

                    # We reload the cleaned CSV from the temporary file
                    cleaned_csv = pd.read_csv("tests/output.tmp.csv")

                    # We create the same output with the CLI and compare
                    # the results

                    status = subprocess.run(
                        [
                            "csv-trim",
                            path,
                            "tests/output.tmp.cli.csv",
                            *(("--no-restore-header",) if not restore_header else ()),
                            *(("--keep-padding",) if not drop_padding else ()),
                            *(("--keep-duplicated-schema",) if not drop_duplicated_schema else ()),
                        ],
                        check=True,
                    )

                    assert status.returncode == 0

                    cli_cleaned_csv = pd.read_csv("tests/output.tmp.cli.csv")

                    assert cleaned_csv.equals(cli_cleaned_csv)

                    # We remove the temporary files
                    os.remove("tests/output.tmp.cli.csv")
                    os.remove("tests/output.tmp.csv")

