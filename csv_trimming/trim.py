"""Module handling the cleaning up of malformed CSVs using heuristics."""

from typing import Tuple, Any, Optional, Callable
import pandas as pd
import numpy as np
from csv_trimming.logger import logger

NAN_LIKE = (
    "",
    0,
    "#RIF!",
    "#N/D",
    None,
    "\n",
    "\r",
    "NaN",
    "?",
    "_",
    "Nan",
    "/",
    " ",
    "-",
    "0",
    "NA",
    ".",
)


def is_nan(candidate: Any) -> bool:
    """Return True if the given candidate is NaN-like.

    Parameters
    ---------------------------
    candidate: object,
        candidate to be checked.

    Returns
    ---------------------------
    True if the given candidate is NaN-like.
    """
    return (
        pd.isna(candidate)
        or candidate in NAN_LIKE
        or isinstance(candidate, str)
        and len(candidate) > 1
        and all(is_nan(e) for e in candidate)
    )


class CSVTrimmer:
    """Class handling the cleaning up of malformed CSVs using heuristics."""

    SPACES = ("\n\r", "\n", " ")

    def __init__(
        self,
        correlation_callback: Optional[
            Callable[[pd.Series, pd.Series], Tuple[bool, pd.Series]]
        ] = None,
    ):
        """Create new CVSTrimmer object.

        Parameters
        ---------------------------
        correlation_callback: Optional[Callable] = None,
            Callback to use to check if two rows required to be specially handled for correlations.
        """
        self._correlation_callback = correlation_callback

    def _mask_edges(self, mask: np.ndarray) -> np.ndarray:
        """ "Return boolean array with only boolean True attached to sides.

        Parameters
        -------------------------------
        mask: np.ndarray,
            Boolean vector from which to extract borders.

        Returns
        -------------------------------
        Boolean array with only boolean True attached to array sides.
        """
        left, right = 0, 0
        for left, val in enumerate(mask):
            if not val:
                break
        for right, val in enumerate(np.flip(mask, axis=0)):
            if not val:
                break
        if right == 0:
            mask[left:] = False
        else:
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
        nan_mask = csv.map(is_nan)
        rows_threshold = np.logical_not(nan_mask).sum(axis=1).mean() / 2
        rows_mask = self._mask_edges((~nan_mask).sum(axis=1).values < rows_threshold)
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
            if is_nan(value):
                new_sanitized_header.append(f"column {nan_values_count}")
                nan_values_count += 1
                continue

            while value in new_sanitized_header:
                value = f"{value}.duplicated"

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
        nan_mask = csv.map(is_nan).all(axis=0)
        return csv[csv.columns[~nan_mask]]

    def drop_duplicated_schema(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return DataFrame with removed duplicated schema.

        Implementative details
        ---------------------------
        In some cases, such as when multiple CSVs are chained in a poor manner,
        the same schema can be repeated multiple times. This method removes
        the duplicated schema if it is detected.
        """
        schema = csv.columns
        for i, row in csv.iterrows():
            if all(row == schema):
                return csv.iloc[:i]
        return csv

    def drop_empty_rows(self, csv: pd.DataFrame) -> pd.DataFrame:
        """Return DataFrame with removed empty columns.

        Parameters
        ---------------------------
        csv: pd.DataFrame,
            DataFrame where to drop the empty columns.

        Returns
        ---------------------------
        DataFrame without empty columns.
        """
        nan_mask = csv.map(is_nan).all(axis=1)
        return csv[~nan_mask]

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
            string = " ".join([e for e in string.split(char) if e])
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
        return csv.map(lambda x: self._deep_strip(x) if isinstance(x, str) else x)

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
        nan_mask = csv.map(is_nan)
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
            csv[:-1].iterrows(), csv[1:].iterrows()
        ):
            if skip_row:
                skip_row = False
                continue
            skip_row, result = self._correlation_callback(current_row, next_row)
            new_rows.append(result)

        if not skip_row:
            new_rows.append(csv.iloc[-1])

        return pd.DataFrame(new_rows)

    def trim(
        self,
        csv: pd.DataFrame,
        drop_duplicated_schema: bool = True,
    ) -> pd.DataFrame:
        """Return sanitized version of given dataframe.

        Parameters
        ----------------------------
        csv: pd.DataFrame,
            The dataframe to clean up.
        drop_duplicated_schema: bool = True,
            Whether to drop duplicated schemas.

        Returns
        ----------------------------
        The cleaned up dataframe.
        """
        logger.info("Removing extra spaces within cells.")
        csv = self.trim_spaces(csv)
        logger.info("Removing empty space (or NaNs).")
        csv = self.trim_padding(csv)
        logger.info("Removing empty space rows.")
        csv = self.drop_empty_rows(csv)
        logger.info("Restoring detected header.")
        csv = self.restore_header(csv)
        logger.info("Restoring true NaN values.")
        csv = self.restore_true_nan(csv)
        logger.info("Normalizing correlated rows (if lambda is provided).")
        csv = self.normalize_correlated_rows(csv)
        logger.info("Dropping empty columns.")
        csv = self.drop_empty_columns(csv)
        if drop_duplicated_schema:
            logger.info("Dropping rows containing duplicated schema.")
            csv = self.drop_duplicated_schema(csv)

        csv = csv.reset_index(drop=True)
        csv.index.name = None
        csv.columns.name = None
        return csv
