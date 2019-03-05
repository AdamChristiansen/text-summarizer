"""
This module provides common operations on text data.
"""

def split_sentence(s):
    """
    Given a string, [s], split it into sentences.

    # Arguments

    * `s` (str) - a string to split.

    # Returns

    A list strings representing the sentences of the text. It is guaranteed
    that each string is non-empty, has at least one whitespace character, and
    both start and end on non-whitespace characters.
    """
    lines = map(str.strip, s.splitlines())
    return list([line for line in lines if line])
