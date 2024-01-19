"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import utils.clean as clean
import utils.log as log


def load_data(*args, **kwargs):
    """
    Wrapper for clean.load_data().
    """
    log.log_step('Import data.')
    f = clean.load_data
    return log.log_wrapper(f, args, kwargs)


def add_to_dataframe(*args, **kwargs):
    """
    Wrapper for clean.add_to_dataframe().
    """
    log.log_step('Add data to dataframe.')
    f = clean.add_to_dataframe
    df = log.log_wrapper(f, args, kwargs)
    log.log_dataframe_contents(df)
    return df


def check_for_missing_data(*args, **kwargs):
    """
    Wrapper for clean.check_for_missing_data().
    """
    log.log_step('Record missing data.')
    # Assume that the dataframe is the first arg.
    log.log_dataframe_contents(args[0])
    f = clean.check_for_missing_data
    return log.log_wrapper(f, args, kwargs)


def apply_one_hot_encoding(*args, **kwargs):
    """
    Wrapper for clean.apply_one_hot_encoding().
    """
    # Set up string for log.log_step().
    # Assume that the series is the first arg.
    series = args[0]
    series_name = log.find_arg_name(series)

    log.log_step(f'{series_name}: one-hot-encode.')
    f = clean.apply_one_hot_encoding
    return log.log_wrapper(f, args, kwargs)


def remove_one_hot_encoding(*args, **kwargs):
    """
    Wrapper for clean.remove_one_hot_encoding().
    """
    # Take the first column name for the label.
    # Assume that columns were given as the second arg.
    cols = args[1]
    col1_name = cols[0]

    log.log_step(f'{col1_name} etc.: remove one-hot-encoding.')
    f = clean.remove_one_hot_encoding
    return log.log_wrapper(f, args, kwargs)


def rename_values(*args, **kwargs):
    """
    Wrapper for clean.rename_values().
    """
    # Set up string for log.log_step().
    # Assume that the series is the first arg.
    series = args[0]
    series_name = log.find_arg_name(series)

    log.log_step(f'{series_name}: rename values.')
    f = clean.rename_values
    return log.log_wrapper(f, args, kwargs)


def split_strings_to_columns_by_delimiter(*args, **kwargs):
    """
    Wrapper for clean.split_strings_to_columns_by_delimiter().
    """
    # Set up string for log.log_step().
    # Assume that the series is the first arg.
    series = args[0]
    series_name = log.find_arg_name(series)

    log.log_step(f'{series_name}: split into multiple columns.')
    f = clean.split_strings_to_columns_by_delimiter
    return log.log_wrapper(f, args, kwargs)


def split_strings_to_columns_by_index(*args, **kwargs):
    """
    Wrapper for clean.split_strings_to_columns_by_index().
    """
    # Set up string for log.log_step().
    # Assume that the series is the first arg.
    series = args[0]
    series_name = log.find_arg_name(series)

    log.log_step(f'{series_name}: split into multiple columns.')
    f = clean.split_strings_to_columns_by_index
    return log.log_wrapper(f, args, kwargs)


def impute_missing_with_median(*args, **kwargs):
    """
    Wrapper for clean.impute_missing_with_median().
    """
    # Set up string for log.log_step().
    # Assume that the series is the first arg.
    series = args[0]
    series_name = log.find_arg_name(series)

    log.log_step(f'{series_name}: impute missing values with median.')
    f = clean.impute_missing_with_median
    return log.log_wrapper(f, args, kwargs)


def impute_missing_with_label(*args, **kwargs):
    """
    Wrapper for clean.imput_missing_with_missing_label().
    """
    # Set up string for log.log_step().
    # Assume that the series is the first arg.
    series = args[0]
    series_name = log.find_arg_name(series)

    log.log_step(f'{series_name}: impute missing values with label.')
    f = clean.impute_missing_with_label
    return log.log_wrapper(f, args, kwargs)


def set_attrs_name(*args, **kwargs):
    """
    Wrapper for clean.set_attrs_name().

    TO DO - find a better home for this!
    """
    f = clean.set_attrs_name
    return log.log_wrapper(f, args, kwargs)
