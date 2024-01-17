"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd


def load_data(path_to_file):
    """Import tabular data from csv."""
    return pd.read_csv(path_to_file)


def check_for_missing_data(df: pd.DataFrame):
    """
    Find number of missing entries in each column of DataFrame.

    Inputs
    ------
    df - pd.DataFrame. DataFrame to be checked for missing entries.

    Returns
    -------
    series_missing - pd.Series. Has an entry for each column of df
                        and its number of missing data points.
    """
    # Make Series with index containing column names from df
    # and first column containing number of missing entries
    # in each column of df.
    series_missing = df.isna().sum()

    # # Set the series name:
    series_missing.name = 'missing_data'
    return series_missing


def apply_one_hot_encoding(series: pd.Series, **kwargs):
    """
    Convert a single column to several one-hot encoded columns.

    Wrapper for pd.get_dummies().

    kwargs for pd.get_dummies():
    + prefix: str, list of str, or dict of str, default None
    + prefix_sep: str, default '_'
    + dummy_na: bool, default False
    + columns: list-like, default None
    + sparse: bool, default False
    + drop_first: bool, default False
    + dtype: dtype, default bool

    Example:
    +----+           +----+----+----+----+
    | c5 |           | c1 | c2 | c3 | c4 |
    +----+           +----+----+----+----+
    | c2 |           |  0 |  1 |  0 |  0 |
    | c1 |    -->    |  1 |  0 |  0 |  0 |
    | c2 |           |  0 |  1 |  0 |  0 |
    | c4 |           |  0 |  0 |  0 |  1 |
    +----+           +----+----+----+----+

    Inputs
    ------
    series   - pd.Series. Column of data to be one-hot-encoded.
    **kwargs - dict. Keyword arguments for pd.get_dummies().

    Returns
    -------
    series_ohe - pd.Series. Several columns, now one-hot-encoded.
    """
    # One-hot-encode the series:
    # TO DO - fix this kwargs argument.
    # TypeError: get_dummies() got an unexpected keyword argument 'kwargs'
    df_ohe = pd.get_dummies(series)#, **kwargs)

    # Set the DataFrame name:
    df_ohe.attrs['name'] = 'ohe'

    return df_ohe


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


def split_strings_to_columns_by_delimiter(
        series: pd.Series, delimiter: str = ','):
    """
    Split column strings by a delimiter, store in multiple columns.

    Wrapper for pd.Series.str.split()

    Example, for delimiter " ":
    +------------------+           +-------+--------------+
    | 42               |           | 42_0  | 42_1         |
    +------------------+           +-------+--------------+
    | "the answer"     |           | "the" | "answer"     |
    | "to life"        |    -->    | "to"  | "life"       |
    | "the universe"   |           | "the" | "universe"   |
    | "and everything" |           | "and" | "everything" |
    +------------------+           +-------+--------------+

    Missing values are unaffected by this. All of the new columns
    for a missing data point will contain only missing values.

    Inputs
    ------
    series    - pd.Series. The column to be split.
    delimiter - str. Move to the next column whenever this delimiter
                is met.

    Returns
    -------
    df_split - pd.DataFrame. DataFrame of many columns containing the
               split strings.
    """
    # Split each cell into multiple columns, one new column for
    # each delimiter hit in the original string.
    df_split = series.str.split(delimiter, expand=True)

    # Label the new columns for the original series name.
    # Results in names "{series.name}_0", "{series.name}_1" etc.
    df_split.columns = [f'{series.name}_{i}' for i in df_split.columns]

    return df_split


def split_strings_to_columns_by_index(
        series: pd.Series, split_index: 'int | list'):
    """
    Split column strings at given indices, store in multiple columns.

    Example, for index 5:
    +------------------+           +---------+-------------+
    | 42               |           | 42_0    | 42_1        |
    +------------------+           +---------+-------------+
    | "the answer"     |           | "the a" | "nswer"     |
    | "to life"        |    -->    | "to li" | "fe"        |
    | "the universe"   |           | "the u" | "niverse"   |
    | "and everything" |           | "and e" | "verything" |
    +------------------+           +---------+-------------+

    Missing values are unaffected by this. All of the new columns
    for a missing data point will contain only missing values.

    Inputs
    ------
    series      - pd.Series. The column to be split.
    split_index - int or list. Cutoff points for the string splits.
                  e.g. index 5 will split the string after the first
                  five characters.

    Returns
    -------
    df_split - pd.DataFrame. DataFrame of many columns containing the
               split strings.
    """
    # Find the name of the starting series:
    n = series.name

    # If the user gave a single split, put it in a list
    # so that the below loop works:
    if isinstance(split_index, (int, float)):
        split_index = [split_index]

    # Add an extra index so that the final piece of the string
    # is added into the column.
    split_index += [None]

    df_split = pd.DataFrame()
    for i, ind_end in enumerate(split_index):
        if i == 0:
            # Start from the start of the string.
            ind_start = None
        else:
            # Start from the previous cut-off.
            ind_start = split_index[i-1]

        # The contents of this column:
        series_split = series.str[ind_start:ind_end]
        # Set empty strings to missing.
        series_split = series_split.replace('', pd.NA)

        # Place this column in the results DataFrame:
        df_split[f'{n}_{i}'] = series_split

    return df_split


def impute_missing_with_median(_series: pd.Series):
    """
    Replace missing values in a Pandas series with median.

    Returns a comppleted series, and a series shwoing which values are imputed

    Original in Mike A's Titanic preprocessing notebook:
    https://michaelallen1966.github.io/titanic/01_preprocessing.html
    (Accessed 12th January 2024).
    """
    # Copy the series to avoid change to the original series.
    series = _series.copy()
    median = series.median()
    missing = series.isna()
    series[missing] = median

    # Set the series names:
    series.name = 'imputed_with_median'
    missing.name = 'missing_bool'

    return series, missing


def impute_missing_with_missing_label(
        _series: pd.Series,
        label: str = 'missing'
        ):
    """
    Replace missing values in a Pandas series with the text 'missing'

    Original in Mike A's Titanic preprocessing notebook:
    https://michaelallen1966.github.io/titanic/01_preprocessing.html
    (Accessed 12th January 2024).
    """
    # Copy the series to avoid change to the original series.
    series = _series.copy()
    missing = series.isna()
    series[missing] = label

    # Set the series names:
    series.name = 'imputed_with_missing_label'
    missing.name = 'missing_bool'

    return series, missing
