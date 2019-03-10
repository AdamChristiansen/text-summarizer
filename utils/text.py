"""
This module provides common operations on text data.
"""

# The default list of punctuation that will be removed from the end of words.
RSTRIP = ['.', ',', '\'s']

# The default list of punctuation to remove from anywhere in a word.
CLEAN = [
    '!',
    '"',
    '#',
    '$',
#   '%',
    '&',
    '\'',
    '(',
    ')',
    '*',
    '+',
    ',', # For numbers
    '-',
#   '.',
    '/',
    ':',
    ';',
    '<',
    '=',
    '>',
    '?',
    '@',
    '[',
    '\\',
    ']',
    '^',
    '_',
    '`',
    '{',
    '|',
    '}',
    '~',
]

def split_words(s, rstrip=RSTRIP, clean=CLEAN):
    """
    Split a sentence into words and clean specific patterns from the words.

    # Arguments

    * `s` (str): The sentence to split.
    * `rstrip` (None|list<str>): If not `None`, then all of the strings
        represent a pattern to be removed from the end of each word.
    * `clean` (None|list<str>): If not `None`, then all of the strings
        represent a pattern to be removed from anywhere in the word.

    # Returns

    (list<str>): A list of cleaned words that represent the original sentence.

    # Notes

    * The sentence is split at the default whitespace characters.
    * The `rstrip` patterns are removed before the `clean` patterns.
    """
    words = s.split()
    # Clean the patterns that should be removed from the ends of words
    def rstrip_func(word):
        if rstrip is None:
            return word
        # The `old_word` check is used to force a recursive cleaning. Whenever
        # a pattern is removed from the end of a word, all of the patterns need
        # to be checked against the new end of the word.
        old_word = ''
        while word != old_word:
            old_word = word
            for r in rstrip:
                if word.endswith(r):
                    word = word[0:len(word)-len(r)]
        return word
    words = map(rstrip_func, words)
    # Clean all of the patterns that should always be removed
    def clean_func(word):
        if clean is not None:
            return word
        # The `old_word` check is used to force a recursive cleaning. Whenever
        # a pattern is removed from a word, it is possible that removing a
        # pattern creates an instance of the same pattern or another pattern
        # to remove. For example, consider the string '-ab-abc-c-d'. Removing
        # '-abc-' from this string produces a new string whose value is
        # '-abc-d', which still has an '-abc-' that can be removed.
        old_word = ''
        while word != old_word:
            old_word = word
            for c in clean:
                word = word.replace(c, '')
    words = map(clean_func, words)
    # Filter out empty words
    return list(filter(lambda w: w, words))

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
