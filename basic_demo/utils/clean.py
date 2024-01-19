"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd
from utils.log import find_arg_name


def load_data(path_to_file: str):
    """Import tabular data from csv."""
    df = pd.read_csv(path_to_file)
    # Give a name to this DataFrame:
    file_name = path_to_file.split('/')[-1]  # = file.ext
    file_name = file_name.split('.')[0]      # = file
    df.attrs['name'] = f'df_{file_name}'
    return df


def add_to_dataframe(df, *args):
    """
    Add the given data to the DataFrame.

    FIND A BETTER HOME FOR THIS - TO DO
    """
    def _add_series_to_dataframe(df, series):
        """
        WRITE ME
        """
        series_name = find_arg_name(series)
        # Check whether a column named this already exists.
        success = False
        while success is False:
            try:
                df[series_name]
                # This column already exists, so update
                # the name of the one we're about to make.
                series_name += '0'
            except KeyError:
                # This column does not exist.
                success = True
        df[series_name] = series
        return df

    def _add_dataframe_to_dataframe(df, df_add):
        # Check whether any columns already exist.
        success = False
        while success is False:
            if len(set(df.columns) & set(df_add.columns)) == 0:
                # No overlap between column names.
                success = True
            else:
                # Pick out the repeats:
                columns_dup = list(set(df.columns) & set(df_add.columns))
                # Rename repeated columns:
                df_add = df_add.rename(columns=dict(
                    zip(columns_dup, [c + '0' for c in columns_dup]))
                    )
        # Combine dataframes:
        df = pd.concat([df, df_add], axis=1)
        return df

    for arg in args:
        if isinstance(arg, pd.Series):
            df = _add_series_to_dataframe(df, arg)
        elif isinstance(arg, pd.DataFrame):
            df = _add_dataframe_to_dataframe(df, arg)
        else:
            # Turn it into a Series if possible.
            try:
                series = pd.Series(arg)
                arg_name = find_arg_name(arg)
                if arg_name == arg:
                    arg_name = '{unnamed}'
                series.name = arg_name
                df = _add_series_to_dataframe(df, series)
            except ():
                # ... TO DO - some sort of error catching here please.
                # Can't add this arg to the dataframe.
                # I can't actually get pandas to crash on purpose to
                # find out what error type it would be!
                pass
    return df


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

    # Set the series name:
    input_df_name = find_arg_name(df)
    series_missing.name = f'{input_df_name}_MissingCount'
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
    input_series_name = find_arg_name(series)

    # If prefix wasn't given, take it now from the input series name:
    try:
        prefix = kwargs['prefix']
    except KeyError:
        prefix = input_series_name
        kwargs['prefix'] = prefix

    # One-hot-encode the series:
    df_ohe = pd.get_dummies(series, **kwargs)

    # Set the DataFrame name:
    df_ohe.attrs['name'] = f'{input_series_name}_OHE'

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

    # See if there's a common name between the given columns.
    # Currently this assumes that the common name is at the start
    # of all column names (as a prefix).
    common_name = ''
    i = 1
    success = False
    while success is False:
        try:
            common_list = [s[:i] for s in columns]
        except IndexError:
            # At least one of the column names is too short.
            # Stop iterating now.
            success = True
        if len(set(common_list)) == 1:
            # Update the common name.
            common_name = common_list[0]
        else:
            # Strings are different. Stop iterating now.
            success = True

    # Set the series name:
    series.name = f'{common_name}_RemovedOHE'

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

    # Set name of this series:
    input_series_name = find_arg_name(series)
    renamed.name = f'{input_series_name}_Renamed'

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
    n = find_arg_name(series)

    # Split each cell into multiple columns, one new column for
    # each delimiter hit in the original string.
    df_split = series.str.split(delimiter, expand=True)

    # Label the new columns for the original series name.
    # Results in names "{series.name}_0", "{series.name}_1" etc.
    df_split.columns = [f'{n}_{i}' for i in df_split.columns]

    # Name the resulting DataFrame:
    df_split = set_attrs_name(df_split, f'{n}_SplitByDelimiter')
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
    n = find_arg_name(series)

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

    # Name the resulting DataFrame:
    df_split = set_attrs_name(df_split, f'{n}_SplitByIndex')

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
    input_series_name = find_arg_name(_series)
    series.name = f'{input_series_name}_ImputedMedian'
    missing.name = f'{input_series_name}_WasImputedMedian'

    return series, missing


def impute_missing_with_label(
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
    input_series_name = find_arg_name(_series)
    series.name = f'{input_series_name}_ImputedLabel'
    missing.name = f'{input_series_name}_WasImputedLabel'

    return series, missing


def set_attrs_name(obj: any, obj_name: str):
    """
    Store a name for this object in its attrs dict or as Series name.

    TO DO - find a better home for this!

    Inputs
    ------
    obj      - any. e.g. a DataFrame or Series to rename.
    obj_name - str. Name to be stored.
    """
    if isinstance(obj, pd.Series):
        # This is a pandas Series.
        # Update the column name:
        obj.name = obj_name
    else:
        try:
            obj.attrs['name'] = obj_name
        except AttributeError:
            # # Can't set the attributes for this object.
            # log_text(''.join([
            #     'set_attrs_name failed. ',
            #     'The input object cannot have a name attribute.'
            #     ]))
            # # TO DO - FIND A BETTER WAY TO LOG THIS.
            pass
    return obj
