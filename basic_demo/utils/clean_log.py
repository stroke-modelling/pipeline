"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd
import inspect  # help find names for logging

import utils.clean as clean
from utils.log import log_function_info, log_function_params, \
    log_function_output, log_text


def log_wrapper(f, args):
    """
    Write function, parameters, and results to the log file.
    """
    # * Separate args and kwargs for the function:
    # --------------------------------------------
    try:
        # Split off kwargs...
        kwargs = args['kwargs']
        # ... and remove from args.
        args.pop('kwargs')
    except KeyError:
        # No kwargs given.
        # Continue as normal.
        kwargs = {}
    # Make a new dict of args and kwargs combined:
    # (this isn't the same as the input "args" because it's
    # removed a level of nesting dictionaries.)
    argskwargs = args | kwargs

    # * Log the function info and inputs:
    # -----------------------------------
    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        argskwargs
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args, **kwargs)
    if not isinstance(to_return, tuple):
        to_return = (to_return, )

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    # Deliberate gap in the log file:
    log_text('')
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def load_data(path_to_file: str):
    """
    Wrapper for clean.load_path().
    """
    args = locals()
    f = clean.load_data
    to_return = log_wrapper(f, args)
    return to_return


def check_for_missing_data(df: pd.DataFrame):
    """
    Wrapper for clean.check_for_missing_data().
    """
    args = locals()
    f = clean.check_for_missing_data
    to_return = log_wrapper(f, args)
    return to_return


def apply_one_hot_encoding(series: pd.Series, **kwargs):
    """
    Wrapper for clean.apply_one_hot_encoding().
    """
    args = locals()
    f = clean.apply_one_hot_encoding
    to_return = log_wrapper(f, args)
    return to_return


def remove_one_hot_encoding(df: pd.DataFrame, columns: list):
    """
    Wrapper for clean.remove_one_hot_encoding().
    """
    args = locals()
    f = clean.remove_one_hot_encoding
    to_return = log_wrapper(f, args)
    return to_return


def rename_values(series: pd.Series, dict_map: dict):
    """
    Wrapper for clean.rename_values().
    """
    args = locals()
    f = clean.rename_values
    to_return = log_wrapper(f, args)
    return to_return


def split_strings_to_columns_by_delimiter(
        series: pd.Series, delimiter: str = ','):
    """
    Wrapper for clean.split_strings_to_columns_by_delimiter().
    """
    args = locals()
    f = clean.split_strings_to_columns_by_delimiter
    to_return = log_wrapper(f, args)
    return to_return


def split_strings_to_columns_by_index(
        series: pd.Series, split_index: 'int | list'):
    """
    Wrapper for clean.split_strings_to_columns_by_index().
    """
    args = locals()
    f = clean.split_strings_to_columns_by_index
    to_return = log_wrapper(f, args)
    return to_return


def impute_missing_with_median(_series: pd.Series):
    """
    Wrapper for clean.impute_missing_with_median().
    """
    args = locals()
    f = clean.impute_missing_with_median
    to_return = log_wrapper(f, args)
    return to_return


def impute_missing_with_missing_label(
        _series: pd.Series,
        label: str = 'missing'
        ):
    """
    Wrapper for clean.imput_missing_with_missing_label().
    """
    args = locals()
    f = clean.impute_missing_with_missing_label
    to_return = log_wrapper(f, args)
    return to_return


def set_attrs_name(obj: any, obj_name: str):
    """
    Wrapper for clean.set_attrs_name().

    TO DO - find a better home for this!
    """
    args = locals()
    f = clean.set_attrs_name
    to_return = log_wrapper(f, args)
    return to_return
