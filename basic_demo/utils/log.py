"""
Functions to log processes.


    # Have to find the following outside of any other functions
    # to prevent RecursionError.
"""
import pandas as pd
import logging
import inspect  # help find names for logging


# #####################################
# ##### Functions to write to log #####
# #####################################
def log_heading(str: str):
    """
    Add a message to the log.

    The heading displays as:
    #################
    ##### {str} #####
    #################
    """
    # Format the string
    str = (
        '\n' +
        '#' * (len(str) + (5 + 1) * 2) + '\n' +
        '#' * 5 + f' {str} ' + '#' * 5 + '\n' +
        '#' * (len(str) + (5 + 1) * 2)
    )

    if logging.getLogger().hasHandlers():
        # If logging is set up, save to log:
        logger = logging.getLogger('pipeline')
        for line in str.split('\n'):
            logger.info(line)
    else:
        # Don't log the message.
        pass


def log_step(str: str):
    """
    Add a message to the log.

    The step name displays as:
    * {str}
    -------
    """
    # Format the string so it displays as:
    str = f'\n* {str}\n' + '-' * (len(str) + 2)

    if logging.getLogger().hasHandlers():
        # If logging is set up, save to log:
        logger = logging.getLogger('pipeline')
        for line in str.split('\n'):
            logger.info(line)
    else:
        # Don't log the message.
        pass


def log_text(str: str, indent: str=''):
    """
    Add a message to the log.
    """
    if len(indent) > 0:
        str = indent + str.replace('\n', f'\n{indent}')

    if logging.getLogger().hasHandlers():
        # If logging is set up, save to log:
        logger = logging.getLogger('pipeline')
        for line in str.split('\n'):
            width = 100 - len('INFO:pipeline:')
            if len(line) < width:
                logger.info(line)
            else:
                # Split the message across multiple lines.
                while len(line) > 0:
                    logger.info(line[:width])
                    line = line[width:]
    else:
        # Don't log the message.
        pass


# ###########################################
# ##### Functions to gather info to log #####
# ###########################################
def log_dataframe_columns(df):
    """
    Write the columns of this DataFrame.
    """
    str = ''.join([
        'Contents:\n  ',
        ',\n  '.join(df.columns)
    ])
    log_text(str, indent='')


def log_function_info(func_module, func_name, func_doc, argspec_sig):
    """
    TEMPORARY, DELETE ME
    # --- Logging ---
    # Record what's happened in the new series attributes.
    # Starting DataFrame name:
    """
    # Find the module that contains this function.
    # func_module = func.__module__

    # Find the function name and description.
    # func_name = func.__name__
    # Get the docstring as a list, line by line:
    try:
        # func_doc_lines = func.__doc__.split('\n')
        func_doc_lines = func_doc.split('\n')
    except AttributeError:
        # Hit this when the docstring is "NoneType" instead of
        # a string, i.e. there's no docstring for this function.
        func_doc_lines = []

    if len(func_doc_lines) < 1:
        func_doc = '{missing docstring}'
    else:
        # Remove leading and trailing whitespace from each line:
        func_doc_lines = [f.strip() for f in func_doc_lines]
        # Store the first line of the docstring that isn't blank.
        i = 0
        func_doc = func_doc_lines[i]
        success = False
        while success == False:
            i += 1
            if i < len(func_doc_lines):
                func_doc = func_doc_lines[i]
            else:
                # Nothing found. Break the loop.
                success = True
            if len(func_doc) > 0:
                success = True

    indent = ' ' * 2  # Number of spaces per indent

    function_str = f'{func_module}.{func_name}('
    function_str_bits = f'{argspec_sig}'.strip('(').strip(')').split(',')
    function_str_bits = [f'{s.strip()}' for s in function_str_bits]
    function_str = (
        f'{indent}{function_str}' +
        f'\n{indent*2}' +
        f',\n{indent*2}'.join(function_str_bits) +
        f'\n{indent})'
        ) 

    # If logging is set up, save to log:
    log_text('\n'.join([
        func_doc,
        'Run this function:',
        function_str
    ]))


def log_function_params(fullargspec, kwargs):
    """
    # --- Logging ---
    # Record what's happened in the new series attributes.
    # Starting DataFrame name:
    """
    # Check the value of each kwarg.
    kwarg_names = {}
    for key, kwarg in zip(kwargs.keys(), kwargs.values()):
        kwarg_name = find_arg_name(kwarg)
        kwarg_names[key] = kwarg_name

    indent = ' ' * 2  # Number of spaces per indent

    # Get one line per arg or kwarg,
    # "  name=value"
    lines = []
    for a, arg in enumerate(fullargspec[0]):
        try:
            val = kwarg_names[arg]
        except KeyError:
            val='None'
        lines.append(f'{indent}{arg}={val}')

    lines_w = newline_for_width(lines, w=100)

    params_str = ',\n'.join(lines_w)

    # If logging is set up, save to log:
    log_text('\n'.join([
        'With these parameters:',
        params_str
    ]))


def log_function_output(return_tuple):
    """
    # --- Logging ---
    # Record what's happened in the new series attributes.
    # Starting DataFrame name:
    """
    indent = ' ' * 2  # Number of spaces per indent

    # Check the value of each kwarg.
    lines = []
    for arg in return_tuple:
        arg_name = find_arg_name(arg)
        lines.append(f'{indent}{arg_name}')

    lines_w = newline_for_width(lines, w=100)

    outputs_str = ',\n'.join(lines_w)

    # If logging is set up, save to log:
    log_text('\n'.join([
        'Giving the following as output:',
        outputs_str
    ]))


def newline_for_width(lines, w=100, indent='  '):
    """
    
    # Maximum number of characters per line:
    w = 100
    """
    # Make sure lines don't go above a certain length.
    lines_w = []
    for line in lines:
        if len(line) < w:
            # No problem, use the line as it is.
            lines_w.append(line)
        else:
            # Make a new line whenever there's an open bracket:
            line = increase_indent_between_brackets(line)

            # At every comma, create a new line.
            lines_c = line.split(',')
            for l, lc in enumerate(lines_c):
                if l > 0:
                    # If this isn't the first line
                    # (which is the parameter name and already has whitespace)
                    # Remove leading and trailing whitespace:
                    lc = lc.strip()
                # Add indent:
                i = '' if l < 1 else indent * 2
                # Save indented line to list:
                lines_w.append(f'{i}{lc}')
    return lines_w


def find_arg_name(arg):
    if isinstance(arg, pd.Series):
        # This is a pandas Series.
        # Take the name of the Series:
        try:
            arg_name = arg.name
        except (KeyError, AttributeError):
            # No name, so use the value instead.
            arg_name = '{unnamed pd.Series}'
    elif isinstance(arg, pd.DataFrame):
        try:
            # Did we explicitly give this a name?
            arg_name = arg.attrs['name']
        except (KeyError, AttributeError):
            # No name, so use the value instead.
            arg_name = '{unnamed pd.DataFrame}'
    else:
        # Last ditch effort to find a name:
        try:
            # Did we explicitly give this a name?
            arg_name = arg.attrs['name']
        except (KeyError, AttributeError):
            # No name, so use the value instead.
            arg_name = arg
    return arg_name


def increase_indent_between_brackets(line, indent='  '):
    """
    Currently gives fixed indentation level.
    """
    def find_substring(s, ss):
        try:
            i = s.index(ss)
        except ValueError:
            # There are no ss substrings in the string.
            i = -1
        return i

    finished_line = ''

    bracket_list = ['(', '[', '{']
    bracket_close_list = [')', ']', '}']
    i_brackets = [find_substring(line, c) for c in bracket_list]
    while all(i < 0 for i in i_brackets) is False:
        # Until all values in i_brackets are -1.
        # Find the bracket that comes next in the string:
        i_brackets_p = [i if i > 0 else max(i_brackets) + 1 for i in i_brackets]
        ind_next_bracket = i_brackets_p.index(min(i_brackets_p))

        c_next_bracket = bracket_list[ind_next_bracket]
        cc_next_bracket = bracket_close_list[ind_next_bracket]

        i_next_open = line.index(c_next_bracket)
        i_next_close = line.index(cc_next_bracket)

        # Everything before and including the first open bracket...
        line_before = line[:i_next_open + 1]
        # Everything between the brackets...
        line_middle = line[i_next_open + 1:i_next_close]
        # Everything from the close bracket onwards:
        line_after = line[i_next_close:]

        finished_line += line_before + f'\n{indent * 2}'
        line_middle = line_middle.replace('\n', f'\n{indent * 2}')

        line = line_middle + f'\n{indent * 2}' + line_after

        # Recalculate bracket locations:
        i_brackets = [find_substring(line, c) for c in bracket_list]
    finished_line += line
    return finished_line


def set_attrs_name(obj: any, obj_name: str):
    """
    Store a name for this object in its attrs dict or as Series name.
    """
    # * Log the function info and inputs:
    # -----------------------------------
    args = locals()
    f = set_attrs_name

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
    if isinstance(obj, pd.Series):
        # This is a pandas Series.
        # Update the column name:
        obj.name = obj_name
    else:
        try:
            o = obj.attrs
            obj.attrs['name'] = obj_name
        except AttributeError:
            # Can't set the attributes for this object.
            log_text(''.join([
                'set_attrs_name failed. ',
                'The input object cannot have a name attribute.'
                ]))

    # * Log the function outputs:
    # ---------------------------
    to_return = (obj, )
    log_function_output([t for t in to_return])
    if len(to_return) == 1:
        to_return = to_return[0]
    return to_return
