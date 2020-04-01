import pandas as pd
import numpy as np
from italian_csv_type_prediction import TypePredictor
from italian_csv_type_prediction.simple_types.nan_type import NaNType
from scipy.ndimage import gaussian_filter
from scipy.stats import mode


def is_na(df: pd.DataFrame):
    return df.applymap(NaNType().validate)


def mask_edges(mask: np.ndarray):
    left = right = 0
    for val in mask:
        if not val:
            break
        left += 1
    for val in np.flip(mask, axis=0):
        if not val:
            break
        right += 1
    mask[left:-right] = False
    return mask


def _trim_padding(csv: pd.DataFrame) -> pd.DataFrame:
    nan_mask = is_na(csv)
    rows_threshold = np.logical_not(nan_mask).sum(axis=1).mean()/2
    rows_mask = mask_edges(np.logical_not(
        nan_mask).sum(axis=1) < rows_threshold)
    columns_mask = mask_edges(nan_mask.all(axis=0).values)
    return csv[~rows_mask][csv.columns[~columns_mask]]


def trim_padding(csv):
    old_shape = None
    while csv.shape != old_shape:
        old_shape = csv.shape
        csv = _trim_padding(csv)
    return csv


def restore_header(csv: pd.DataFrame) -> pd.DataFrame:
    new_header = csv.iloc[0]  # grab the first row for the header

    new_sanitized_header = []
    nan_values_count = 0
    for value in new_header:
        if pd.isna(value):
            new_sanitized_header.append("column {}".format(nan_values_count))
            nan_values_count += 1
            continue

        while value in new_sanitized_header:
            value = "{}.duplicated".format(value)

        new_sanitized_header.append(value)

    csv = csv[1:]  # take the data less the header row
    csv.columns = new_sanitized_header  # set the header row as the csv header
    return csv


def drop_empty_columns(csv: pd.DataFrame) -> pd.DataFrame:
    nan_mask = is_na(csv).all(axis=0)
    return csv[csv.columns[~nan_mask]]


def deep_strip(string: str):
    for char in ("\n\r", "\n", " "):
        string = " ".join(string.split(char))
    return string.strip()


def trim_spaces(csv):
    return csv.applymap(lambda x: deep_strip(x) if isinstance(x, str) else x)


def restore_true_nan(csv: pd.DataFrame):
    nan_mask = TypePredictor().predict_dataframe(csv) == "NaN"
    return csv.where(np.logical_not(nan_mask))


def trim_csv(csv: pd.DataFrame):
    csv = trim_spaces(csv)
    csv = trim_padding(csv)
    csv = restore_header(csv)
    csv = restore_true_nan(csv)
    csv = drop_empty_columns(csv)
    csv = csv.reset_index(drop=True)
    csv.index.name = None
    csv.columns.name = None
    return csv
