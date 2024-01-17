"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd
import inspect  # help find names for logging

import utils.clean as clean
from utils.log import log_function_info, log_function_params, \
    log_function_output


def load_data(path_to_file):
    """
    Wrapper for clean.load_path().

    Don't bother to write this info to the log.
    TO DO - or do? Log the file name.
    """
    return clean.load_data(path_to_file)


def check_for_missing_data(df: pd.DataFrame):
    """
    Wrapper for clean.check_for_missing_data().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.check_for_missing_data

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def apply_one_hot_encoding(series: pd.Series, **kwargs):
    """
    Wrapper for clean.apply_one_hot_encoding().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.apply_one_hot_encoding

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def remove_one_hot_encoding(df: pd.DataFrame, columns: list):
    """
    Wrapper for clean.remove_one_hot_encoding().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.remove_one_hot_encoding

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def rename_values(series: pd.Series, dict_map: dict):
    """
    Wrapper for clean.rename_values().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.rename_values

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def split_strings_to_columns_by_delimiter(
        series: pd.Series, delimiter: str = ','):
    """
    Wrapper for clean.split_strings_to_columns_by_delimiter().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.split_strings_to_columns_by_delimiter

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def split_strings_to_columns_by_index(
        series: pd.Series, split_index: 'int | list'):
    """
    Wrapper for clean.split_strings_to_columns_by_index().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.split_strings_to_columns_by_index

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def impute_missing_with_median(_series: pd.Series):
    """
    Wrapper for clean.impute_missing_with_median().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.impute_missing_with_median

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return


def impute_missing_with_missing_label(
        _series: pd.Series,
        label: str = 'missing'
        ):
    """
    Wrapper for clean.imput_missing_with_missing_label().
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = clean.impute_missing_with_missing_label

    log_function_info(
        f.__module__,
        f.__name__,
        f.__doc__,
        inspect.signature(f)
        )
    log_function_params(
        inspect.getfullargspec(f),
        args
        )

    # * The actual calculations:
    # --------------------------
    to_return = f(**args)

    # * Log the function outputs:
    # ---------------------------
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return
