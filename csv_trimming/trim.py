import pandas as pd
import numpy as np
from italian_csv_type_prediction import TypePredictor
from italian_csv_type_prediction.simple_types.nan_type import NaNType
from scipy.ndimage import gaussian_filter
from scipy.stats import mode
from typing import Callable


class CSVTrimmer:
    """Class handling the cleaning up of malformed CSVs using heuristics."""

    SPACES = "\n\r", "\n", " "

    def __init__(self, correlation_callback: Callable[[pd.Series, pd.Series], bool] = None):
        """Create new CVSTrimmer object.

        Parameters
        ---------------------------
        correlation_callback: Callable = None,
            Callback to use to check if two rows required to be specially handled for correlations.
        """
        self._correlation_callback = correlation_callback
        self._nan_type = NaNType()
        self._type_predictor = TypePredictor()

    def _mask_edges(self, mask: np.ndarray) -> np.ndarray:
        """"Return boolean array with only boolean True attached to sides.

        Parameters
        -------------------------------
        mask: np.ndarray,
            Boolean vector from which to extract borders.

        Returns
        -------------------------------
        Boolean array with only boolean True attached to array sides.
        """
        for left, val in enumerate(mask):
            if not val:
                break
        for right, val in enumerate(np.flip(mask, axis=0)):
            if not val:
                break
        mask[left:-right] = False
        return mask

    def trim_padding(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return given CSV with trimmed rows and columns.

        Parameters
        -------------------------------
        csv: pd.DataFrame,
            DataFrame whose borders are to be cleaned up.

        Returns
        -------------------------------
        DataFrame wthout empty or near-empty border columns.
        """
        old_shape = None
        while csv.shape != old_shape:
            old_shape = csv.shape
            nan_mask = csv.applymap(self._nan_type.validate)
            rows_threshold = np.logical_not(nan_mask).sum(axis=1).mean()/2
            rows_mask = self._mask_edges(np.logical_not(
                nan_mask).sum(axis=1) < rows_threshold)
            columns_mask = self._mask_edges(nan_mask.all(axis=0).values)
            csv = csv[~rows_mask][csv.columns[~columns_mask]]
        return csv

    def restore_header(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return CSV with restored first row as header of CSV.

        Eventual double columns have added the term '.duplicated'.
        Eventual columns without name are called 'column #n'

        Parameters
        -------------------------------
        csv: pd.DataFrame,
            DataFrame where to restore the header.

        Returns
        -------------------------------
        DataFrame with restored header.
        """
        new_header = csv.iloc[0]  # grab the first row for the header

        new_sanitized_header = []
        nan_values_count = 0
        for value in new_header:
            if pd.isna(value):
                new_sanitized_header.append(
                    "column {}".format(nan_values_count))
                nan_values_count += 1
                continue

            while value in new_sanitized_header:
                value = "{}.duplicated".format(value)

            new_sanitized_header.append(value)

        csv = csv[1:]  # take the data less the header row
        csv.columns = new_sanitized_header  # set the header row as the csv header
        return csv

    def drop_empty_columns(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return DataFrame with removed empty columns.

        Parameters
        ---------------------------
        csv: pd.DataFrame,
            DataFrame where to drop the empty columns.

        Returns
        ---------------------------
        DataFrame without empty columns.
        """
        nan_mask = csv.applymap(self._nan_type.validate).all(axis=0)
        return csv[csv.columns[~nan_mask]]

    def _deep_strip(self, string: str):
        """Return string without continuos spaces.

        Parameters
        ----------------------------
        string: str,
            Sanitized string.

        Returns
        ----------------------------
        String without duplicated spaces.
        """
        for char in CSVTrimmer.SPACES:
            string = " ".join([
                e
                for e in string.split(char)
                if e
            ])
        return string.strip()

    def trim_spaces(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return dataframe without multiple spaces.

        Parameters
        ---------------------------
        csv: pd.DataFrame,
            DataFrame to be sanitized.

        Returns
        ---------------------------
        DataFrame without multiple spaces in strings.
        """
        return csv.applymap(
            lambda x: self._deep_strip(x) if isinstance(x, str) else x
        )

    def restore_true_nan(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return CSV with restored True NaN values.

        Parameters
        ----------------------------
        csv: pd.DataFrame,
            DataFrame where to restore the NaN values.

        Returns
        ----------------------------
        DataFrame with restored NaN values.
        """
        nan_mask = self._type_predictor.predict_dataframe(csv) == "NaN"
        return csv.where(np.logical_not(nan_mask))

    def normalize_correlated_rows(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return normalized correlated rows.
        
        Parameters
        --------------------------
        csv: pd.DataFrame,
            DataFrame to be normalized.

        Returns
        --------------------------
        The dataframe normalized correlated rows.
        """
        if self._correlation_callback is None:
            return csv

        new_rows = []
        skip_row = False

        for (_, current_row), (_, next_row) in zip(
            csv[:-1].iterrows(),
            csv[1:].iterrows()
        ):
            if skip_row:
                skip_row = False
                continue
            if self._correlation_callback(current_row, next_row):
                new_rows.append(pd.concat([
                    current_row, pd.Series({
                        "correlated_{}".format(column): value
                        for column, value in next_row.items()
                    })
                ]))
                skip_row = True
            else:
                new_rows.append(current_row)

        return pd.DataFrame(new_rows)

    def trim(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return sanitized version of given dataframe.

        Parameters
        ----------------------------
        csv: pd.DataFrame,
            The dataframe to clean up.

        Returns
        ----------------------------
        The cleaned up dataframe.
        """
        csv = self.trim_spaces(csv)
        csv = self.trim_padding(csv)
        csv = self.restore_header(csv)
        csv = self.restore_true_nan(csv)

        csv = self.normalize_correlated_rows(csv)

        csv = self.drop_empty_columns(csv)
        csv = csv.reset_index(drop=True)
        csv.index.name = None
        csv.columns.name = None
        return csv
