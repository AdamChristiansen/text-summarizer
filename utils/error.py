"""
This module provides means for issuing errors and warnings.
"""

import sys

import utils.color as color

def error(message, reason=None, warning=False):
    """
    Print an error message and exit the program.

    # Arguments

    * `message` (str): The error message.
    * `reason` (str|None): An optional reason for why the error occurred.
    * `warning` (bool): Demotes the error to a warning, which changes the
        style and prevents the program from terminating.
    """
    p = []
    if warning:
        p.append(color.yel("Warning"))
    else:
        p.append(color.red("Error"))
    p.append(": ")
    p.append(message.strip())
    if reason is not None:
        p.append(": ")
        p.append(color.blk(reason.strip()))
    print(''.join(p))
    if not warning:
        sys.exit(1)
