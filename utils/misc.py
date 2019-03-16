"""
This module provides functions that do not fit anywhere else.
"""

def str_to_bool(s):
    """
    Converts a string to a boolean.

    # Arguments

    * `s` (str): The string to convert.

    # Returns

    (bool): The boolean representation of the string.

    # Raises

    * (ValueError): The string cannot be converted to a boolean.
    """
    s = s.lower()
    if s in ['0', 'false', 'f']:
        return False
    elif s in ['1', 'true', 't']:
        return True
    else:
        raise ValueError(f"Invalid value: {s}")
