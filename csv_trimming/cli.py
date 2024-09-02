"""CLI command and entry point"""

import argparse
import pandas as pd
from csv_trimming import CSVTrimmer


def main():
    """CLI command and entry point"""
    parser = argparse.ArgumentParser(
        description="Clean up malformed CSV files using heuristics."
    )

    parser.add_argument("input_csv", help="Path to the input CSV file.")
    parser.add_argument("output_csv", help="Path to save the cleaned CSV file.")
    parser.add_argument(
        "--no-restore-header",
        action="store_true",
        help="Does not attempt to restore the header.",
        default=False,
    )
    parser.add_argument(
        "--keep-padding",
        action="store_true",
        help="Does not attempt to drop padding.",
        default=False,
    )
    parser.add_argument(
        "--keep-duplicated-schema",
        action="store_true",
        help="Does not attempt to drop duplicated schema.",
        default=False,
    )

    args = parser.parse_args()

    # Load the CSV file
    csv = pd.read_csv(args.input_csv)

    # Create the CSVTrimmer object
    trimmer = CSVTrimmer()

    # Clean up the CSV using the options provided
    cleaned_csv = trimmer.trim(
        csv,
        restore_header=not args.no_restore_header,
        drop_padding=not args.keep_padding,
        drop_duplicated_schema=not args.keep_duplicated_schema,
    )

    # Save the cleaned CSV
    cleaned_csv.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
