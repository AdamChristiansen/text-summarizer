"""
This module provides common file system operations.
"""

import os

def symmetric_dir_contents(d1_path, d2_path, files=False, dirs=False,
        hidden=False):
    """
    Get the contents of two directories, and return those items in each
    directory. Additionally, a warning is printed with the missing files.

    # Arguments

    * `d1_path` (str): That path to the first directory.
    * `d2_path` (str): That path to the second directory.
    * `files` (bool): Indicates that files should be returned.
    * `dirs` (bool): Indicates that directories should be returned.
    * `hidden` (bool): Indicates that hidden items should be returned.

    # Returns

    (list<str>): A sorted list of the item names that are present in both
    directories.
    """

    def key(path, fname):
        """
        The key to use to determine whether an item is included in the search
        result.

        # Arguments

        * `path` (str): The path the file is in.
        * `fname` (str): The name of the file.

        # Returns

        (bool): Indicates whether the item name should be included in the
        result.
        """
        fname_abs = os.path.join(path, fname)
        include_file = files and os.path.isfile(fname_abs)
        include_dir  = dirs  and os.path.isdir(fname_abs)
        include_hidden = hidden and fname.startswith('.')
        return include_file or include_dir or include_hidden

    def dir_items(path):
        """
        Get all items in a directory.

        # Arguments

        * `path` (str): The path to the directory.

        # Returns

        (set<str>): A set of the item names in the path.
        """
        items = []
        for fname in os.listdir(path):
            if key(path, fname):
                items.append(fname)
        return set(items)

    f1 = dir_items(d1_path)
    f2 = dir_items(d2_path)

    f1_not_in_f2 = sorted(f1 - f2)
    f2_not_in_f1 = sorted(f2 - f1)
    f12          = sorted(f1.intersection(f2))

    def print_missing(missing, need, have):
        """
        Print the missing files.

        # Arguments

        * `missing` (iterable<str>): The file names that are missing from the
            directory.
        * `need` (str): The directory which needs the missing items.
        * `have` (str): The directory which has the missing items.
        """
        if missing:
            print(f"Directory {clr.blu(have)} has the following files/" +
                    f"directories that are missing from {clr.blu(need)}:")
            for m in missing:
                print(clr.red(f"    {m}"))
            print("These files/directories will be skipped.")
            print()

    print_missing(f1_not_in_f2, d1_path, d2_path)
    print_missing(f2_not_in_f1, d2_path, d1_path)

    return f12
