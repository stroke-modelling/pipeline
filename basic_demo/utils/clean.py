"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd


def load_data(path_to_file):
    """Import tabular data from csv."""
    return pd.read_csv(path_to_file)


def remove_one_hot_encoding(df: pd.DataFrame, columns: list):
    """
    Convert one-hot-encoded DataFrame columns to one Series.

    The resulting column's values may be any column name of the
    original dataframe.

    Example:
    +----+----+----+----+           +----+
    | c1 | c2 | c3 | c4 |           | c5 |
    +----+----+----+----+           +----+
    |  0 |  1 |  0 |  0 |           | c2 |
    |  1 |  0 |  0 |  0 |    -->    | c1 |
    |  0 |  1 |  0 |  0 |           | c2 |
    |  0 |  0 |  0 |  1 |           | c4 |
    +----+----+----+----+           +----+

    Based on Amy H's work on cleaning SSNAP data, specifically
    converting one-hot columns containing age bands to a single age
    band column.
    Original file's location (accessed 8th January 2024):
    samuel-book (branch: main)
      > samuel_2_data_prep
        > 01_clean_raw_data.ipynb

    Inputs
    ------
    df      - pd.DataFrame. Contains one-hot-encoded columns.
    columns - list. Names of the one-hot-encoded columns.

    Returns
    -------
    series - pd.Series. Each row contains the name of the column
             that had the highest value for that row. For one-hot-
             encoded data, expect all but one values in a row to be 0.
    """
    # Extract columns
    col_extract: pd.DataFrame = df[columns]
    # Find which column contains the highest value for each patient.
    # Expect most rows to contain one 1 and the rest 0.
    series: pd.Series = col_extract.idxmax(axis=1)
    # The values in this Series are the column names from df.
    # The values in col_extract and df remain unchanged.

    # Set the series name:
    series.name = 'removed_one_hot'
    return series


def rename_values(series: pd.Series, dict_map: dict):
    """
    Make a copy of a pd.Series with the values renamed.

    Example:
    +--------+           +---------+
    | series |           | renamed |
    +--------+           +---------+
    |    F   |           |    0    |
    |    M   |    -->    |    1    |
    |    F   |           |    0    |
    |    F   |           |    0    |
    +--------+           +---------+

    Based on Amy H's work on cleaning SSNAP data, for example
    converting "M" and "F" strings to 1 and 0 integers respectively.
    Original file's location (accessed 8th January 2024):
    samuel-book (branch: main)
      > samuel_2_data_prep
        > 01_clean_raw_data.ipynb

    Example dictionary map to match gender M/F to 1/0:
      dict_map: dict = {'M': 1, 'F': 0}
    """
    # The "series" object is not changed. The "renamed" object
    # is a copy of the "series" object with the values renamed.
    renamed: pd.Series = series.map(dict_map)
    return renamed
