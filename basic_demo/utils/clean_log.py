"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd

import utils.clean as clean
from utils.log import log_wrapper


def load_data(*args, **kwargs):
    """
    Wrapper for clean.load_path().
    """
    f = clean.load_data
    return log_wrapper(f, args, kwargs)


def check_for_missing_data(*args, **kwargs):
    """
    Wrapper for clean.check_for_missing_data().
    """
    f = clean.check_for_missing_data
    return log_wrapper(f, args, kwargs)


def apply_one_hot_encoding(*args, **kwargs):
    """
    Wrapper for clean.apply_one_hot_encoding().
    """
    f = clean.apply_one_hot_encoding
    return log_wrapper(f, args, kwargs)


def remove_one_hot_encoding(*args, **kwargs):
    """
    Wrapper for clean.remove_one_hot_encoding().
    """
    f = clean.remove_one_hot_encoding
    return log_wrapper(f, args, kwargs)


def rename_values(*args, **kwargs):
    """
    Wrapper for clean.rename_values().
    """
    f = clean.rename_values
    return log_wrapper(f, args, kwargs)


def split_strings_to_columns_by_delimiter(*args, **kwargs):
    """
    Wrapper for clean.split_strings_to_columns_by_delimiter().
    """
    f = clean.split_strings_to_columns_by_delimiter
    return log_wrapper(f, args, kwargs)


def split_strings_to_columns_by_index(*args, **kwargs):
    """
    Wrapper for clean.split_strings_to_columns_by_index().
    """
    f = clean.split_strings_to_columns_by_index
    return log_wrapper(f, args, kwargs)


def impute_missing_with_median(*args, **kwargs):
    """
    Wrapper for clean.impute_missing_with_median().
    """
    f = clean.impute_missing_with_median
    return log_wrapper(f, args, kwargs)


def impute_missing_with_missing_label(*args, **kwargs):
    """
    Wrapper for clean.imput_missing_with_missing_label().
    """
    f = clean.impute_missing_with_missing_label
    return log_wrapper(f, args, kwargs)


def set_attrs_name(*args, **kwargs):
    """
    Wrapper for clean.set_attrs_name().

    TO DO - find a better home for this!
    """
    f = clean.set_attrs_name
    return log_wrapper(f, args, kwargs)
