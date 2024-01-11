"""
Functions to log processes.
"""
import pandas as pd


def set_attrs_name(obj: any, obj_name: str):
    """
    Store a name for this object in its attrs dict or as Series name.
    """
    try:
        o = obj.attrs
    except AttributeError:
        # Can't set the attributes for this object.
        return obj
        # TO DO - LOG THIS FAILURE

    if isinstance(obj, pd.Series):
        # This is a pandas Series.
        # Update the column name:
        obj.name = obj_name
    else:
        obj.attrs['name'] = obj_name
    return obj


def print_dataframe_columns(df):
    str = ''.join([
        'Contents:\n  ',
        ',\n  '.join(df.columns)
    ])
    write_to_log(str, indent='')


def log(func, args=[], kwargs={}):
    """
    # --- Logging ---
    # Record what's happened in the new series attributes.
    # Starting DataFrame name:
    """
    # Find the module that contains this function.
    func_module = func.__module__

    # Find the function name and description.
    func_name = func.__name__
    # Get the docstring as a list, line by line:
    try:
        func_doc_lines = func.__doc__.split('\n')
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

    # Check the value of each arg.
    arg_names = []
    for arg in args:
        arg_name = find_arg_name(arg)
        arg_names.append(arg_name)

    # Check the value of each kwarg.
    kwarg_names = {}
    for key, kwarg in zip(kwargs.keys(), kwargs.values()):
        kwarg_name = find_arg_name(kwarg)
        kwarg_names[key] = kwarg_name

    args_str = ', '.join([str(a) for a in args])
    kwargs_str = ', '.join(f'{k}={v}' for k, v
                           in zip(kwarg_names.keys(), kwarg_names.values()))

    import inspect
    argspec_sig = inspect.signature(func)

    indent = ' ' * 2  # Number of spaces per indent
    print(func_doc)
    function_str = f'{func_module}.{func_name}('
    function_str_bits = f'{argspec_sig}'.strip('(').strip(')').split(',')
    function_str_bits = [f'{s.strip()}' for s in function_str_bits]
    function_str = (
        f'{indent}{function_str}' +
        f'\n{indent*2}' +
        f',\n{indent*2}'.join(function_str_bits) +
        f'\n{indent})'
        )
    print('Run this function:')
    print(function_str)

    # Get one line per arg or kwarg,
    # "  name=value"
    lines = []
    for a, arg in enumerate(inspect.getfullargspec(func)[0]):
        if a < len(args):
            val = arg_names[a]
        else:
            try:
                val = kwarg_names[arg]
            except KeyError:
                val='None'
        lines.append(f'{indent}{arg}={val}')

    def find_substring(s, ss):
        try:
            i = s.index(ss)
        except ValueError:
            # There are no ss substrings in the string.
            i = -1
        return i

    def increase_indent_between_brackets(line):
        """
        Currently gives fixed indentation level.
        """
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

    # Make sure lines don't go above a certain length.
    # Maximum number of characters per line:
    w = 79
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

    argspec_str2 = ',\n'.join(lines_w)
    print('With these parameters:')
    print(argspec_str2)
    print('')

    # argspec_str = f'{func_module}.{func_name}({args_str}, {kwargs_str})'
    # print(argspec_str)

    # Run the function and immediately return the result:
    return func(*args, **kwargs)


def write_to_log(
        str: str,
        indent: str='  ',
        heading: bool=False,
        step_heading: bool=False
        ):
    """
    Add a message to the log.
    """
    if heading is True:
        # Format the string so it displays as:
        # """
        # #################
        # ##### {str} #####
        # #################
        # """
        str = (
            '\n' +
            '#' * (len(str) + (5 + 1) * 2) + '\n' +
            '#' * 5 + f' {str} ' + '#' * 5 + '\n' +
            '#' * (len(str) + (5 + 1) * 2)
        )
        # Override the indent:
        indent = ''
    elif step_heading is True:
        # Format the string so it displays as:
        # """
        # * {str}
        # -------
        # """
        str = f'\n* {str}\n' + '-' * (len(str) + 2)
        # Override the indent:
        indent = ''
    if len(indent) > 0:
        str = indent + str.replace('\n', f'\n{indent}')
    print(str)
