"""
Routines for cleaning input dataframe.

Assumes that the data is stored as a Pandas DataFrame object.
"""
import pandas as pd

import utils.clean as clean
from utils.log import log_wrapper, log_heading, log_step, log_text, \
    log_dataframe_contents, log_dataframe_stats, find_arg_name


def load_data(*args, **kwargs):
    """
    Wrapper for clean.load_data().
    """
    log_step('Import data.')
    f = clean.load_data
    return log_wrapper(f, args, kwargs)


def check_for_missing_data(*args, **kwargs):
    """
    Wrapper for clean.check_for_missing_data().
    """
    log_step('Record missing data.')
    # Assume that the dataframe is the first arg.
    log_dataframe_contents(args[0])
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
    # Set up string for log_step():
    # Assume that the series is the first arg.
    series = args[0]
    series_name = find_arg_name(series)
    # Assume that the dictionary map is the second arg.
    dict_map = args[1]
    if len(dict_map) == 2:
        # If there are only two things, print it in the
        # log step.
        map_str = ''
        for key, val in zip(dict_map.keys(), dict_map.values()):
            map_str += f', {key} to {val}'
        # Remove first comma.
        map_str = map_str[1:]
    else:
        # If the dictionary is too long, don't print it.
        map_str = ''

    log_step(f'{series_name}: rename values.{map_str}')
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
