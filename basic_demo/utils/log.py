"""
Functions to log processes.

Most of the pipeline functions will have the same few lines
of calls to these log functions within them. This is annoying
but necessary as placing the copied lines in their own function
results in RecursionError. The alternative is forcing the user
to call every function in the form of log(function, parameter_list)
which is harder to read and to reuse elsewhere without the log.
"""
import pandas as pd
import logging
import inspect  # help find names for logging
import io  # To write df.info() output to log.


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


def log_text(str: str, indent: str = '', w=100):
    """
    Add a message to the log.

    If the message is above the set width then it will be split
    across multiple lines.
    """
    if len(indent) > 0:
        str = indent + str.replace('\n', f'\n{indent}')

    if logging.getLogger().hasHandlers():
        # If logging is set up, save to log:
        logger = logging.getLogger('pipeline')
        for line in str.split('\n'):
            width = w - len('INFO:pipeline:')
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
def log_dataframe_contents(df):
    """
    Write the info of this DataFrame - columns, missing, dtype.

    Wrapper for df.info().
    """
    # Send the output of df.info() to this buffer:
    buf = io.StringIO()
    # Get the useful information:
    df.info(
        buf=buf, verbose=True, show_counts=True, memory_usage=False)
    # Convert the contents of the buffer to string so that
    # we can write it to log:
    log_text(buf.getvalue())


def log_dataframe_stats(df):
    """
    Write stats for this DataFrame - mean, std, min...

    Wrapper for df.describe().
    """
    # Get the useful information:
    stats = df.describe()
    # Convert the contents of the buffer to string so that
    # we can write it to log:
    log_text(stats.T.to_string())


def log_function_info(func_module, func_name, func_doc, argspec_sig):
    """
    Log the function module, name, short docstring, and parameter names.

    Inputs
    ------
    func_module - str. The module that contains this function.
    func_name   - str. The name of this function.
    func_doc    - str. The docstring of this function.
    argspec_sig - str. The (param1, param2...) part of the function.

    Result:
    -------
    {first line of docstring}
    Run this function:
      {function module}.{function name}(
        param1: type hint of param1,
        param2: type hint of param2
      )
    """
    # Get the docstring as a list, line by line:
    try:
        func_doc_lines = func_doc.split('\n')
        # Remove leading and trailing whitespace from each line:
        func_doc_lines = [f.strip() for f in func_doc_lines]
    except AttributeError:
        # Hit this when the docstring is "NoneType" instead of
        # a string, i.e. there's no docstring for this function.
        func_doc_lines = []

    if len(func_doc_lines) < 1:
        func_doc = '{missing docstring}'
    else:
        # Store the first line of the docstring that isn't blank.
        i = 0
        success = False
        while not success:
            if i < len(func_doc_lines):
                func_doc = func_doc_lines[i]
                if len(func_doc) > 0:
                    success = True
                else:
                    pass
            else:
                # Nothing found. Break the loop.
                success = True
                func_doc = ''
            i += 1

    indent = ' ' * 2  # Number of spaces per indent

    # Start of the function string:
    function_str = f'{func_module}.{func_name}('
    # Parameter names and types:
    params_str_list = f'{argspec_sig}'.strip('(').strip(')').split(',')
    params_str_list = [f'{s.strip()}' for s in params_str_list]
    params_str = f',\n{indent*2}'.join(params_str_list)
    # Everything together:
    function_str = (
        f'{indent}{function_str}\n' +
        f'{indent*2}{params_str}\n' +
        f'{indent})'
        )

    # If logging is set up, save to log:
    log_text('\n'.join([
        func_doc,
        'Run this function:',
        function_str
    ]))


def log_function_params(fullargspec, kwargs):
    """
    Log the names and values of parameters passed to the function.

    Result:
    -------
    With these parameters:
      param1={value or name of param1}
      param2={value or name of param2}
    """
    # Check the value of each kwarg.
    kwarg_names = {}
    for key, kwarg in zip(kwargs.keys(), kwargs.values()):
        kwarg_name = find_arg_name(kwarg)
        kwarg_names[key] = kwarg_name

    indent = ' ' * 2  # Number of spaces per indent

    # Get one line per arg or kwarg,
    # "  name=value"
    params_str = ''
    for a, arg in enumerate(fullargspec[0]):
        try:
            val = kwarg_names[arg]
        except KeyError:
            val = 'None'
        params_str += f'{indent}{arg}={val},\n'

    params_str = _newline_for_width(params_str, w=100)

    # If logging is set up, save to log:
    log_text('\n'.join([
        'With these parameters:',
        params_str
    ]))


def log_function_output(return_tuple):
    """
    Log the names and values of parameters returned by the function.

    Result:
    -------
    Giving the following as output:
      {value or name of result1}
      {value or name of result2}
    """
    indent = ' ' * 2  # Number of spaces per indent

    # Check the value of each kwarg.
    lines = []
    for arg in return_tuple:
        arg_name = find_arg_name(arg)
        lines.append(f'{indent}{arg_name}')

    lines_w = _newline_for_width(lines, w=100)

    outputs_str = ',\n'.join(lines_w)

    # If logging is set up, save to log:
    log_text('\n'.join([
        'Giving the following as output:',
        outputs_str
    ]))


# ############################
# ##### Helper functions #####
# ############################
def _newline_for_width(line: str, w: int = 100, indent: str = '  '):
    """
    Keep line width down by splitting at brackets and commas.

    This needs fixing - results currently mixed.

    Inputs
    ------
    line   - str. str to shorten.
    w      - int. Maximum number of characters per line:
    indent - str. Plonked on the start of each new line.
    """
    # Make sure lines don't go above a certain length.
    if len(line) < w:
        # No problem, use the line as it is.
        return line
    else:
        line_w = ''
        # Make a new line whenever there's an open bracket:
        line = _increase_indent_between_brackets(line)

        # At every comma, create a new line.
        lines_c = line.split(',')
        for i, lc in enumerate(lines_c):
            if i > 0:
                # If this isn't the first line
                # (which is the parameter name and already has whitespace)
                # Remove leading and trailing whitespace:
                lc = lc.strip()
                # lc = f',\n{i}{lc}'
            # Add indent:
            i = '' if i < 1 else indent * 2
            # Save indented line to list:
            line_w += f',\n{i}{lc}'
    return line_w


def find_arg_name(arg: any):
    """
    Find the name stored in attrs or as Series name.

    Inputs
    ------
    arg - any. Object that we want to find the name of.

    Returns
    -------
    arg_name - str. The name if possible, or a placeholder name
               to prevent printing a huge or sensitive data file,
               or if all else fails then just the value itself.
    """
    if isinstance(arg, pd.Series):
        # This is a pandas Series.
        # Take the name of the Series:
        arg_name = arg.name
        if arg_name is None:
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


def _increase_indent_between_brackets(line, indent='  '):
    """
    Currently gives fixed indentation level.

    This needs fixing - currently has mixed results.
    Ideally would want more indentation for more nested brackets.
    """
    def find_substring(s, ss):
        """Find index in string s where substring ss first appears."""
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
        i_brackets_p = [i if i > 0 else max(i_brackets) + 1
                        for i in i_brackets]
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
    finished_line += str(line)
    return finished_line


def set_attrs_name(obj: any, obj_name: str):
    """
    Store a name for this object in its attrs dict or as Series name.

    Inputs
    ------
    obj      - any. e.g. a DataFrame or Series to rename.
    obj_name - str. Name to be stored.
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
