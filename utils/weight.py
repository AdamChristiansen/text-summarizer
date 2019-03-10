"""
This module defines functions used for assigning sentence weights.
"""

import numpy as np

def __normalize(ws, xs, normalize):
    """
    Normalize an array by its sum.

    # Arguments

    * `ws` (np.array<num>): The original array.
    * `xs` (np.array<num>): The array to be normalized.
    * `normalize` (bool): Indicates that the normalization should be run.

    # Returns

    (np.array<num>): The normalized array.

    # Notes

    For the representation of a sentence, the sum of the occurrences of all
    words is equal to its length. Therefore, when this is applied to a word
    frequency vector this is the same as normalizing the sentence by its
    length.
    """
    if normalize:
        # Note that the sum of the original array is taken, because this is the
        # proper sentence length.
        return xs / np.sum(ws)
    return xs

def __local_none(ws, normalize=False):
    """
    The weight is simply the word frequency.

    # Arguments

    * `ws` (numpy.array<num>): The term frequency vector.
    * `normalize` (bool): Indicates whether the result should be normalized.

    # Returns

    (numpy.array<num>): The weighted term frequency vector.
    """
    return __normalize(ws, ws, normalize)

def __local_binary(ws, normalize=False):
    """
    The weight is binary, so it is 1 if the word is in the sentence and 0 if
    it is not.

    # Arguments

    * `ws` (numpy.array<num>): The term frequency vector.
    * `normalize` (bool): Indicates whether the result should be normalized.

    # Returns

    (numpy.array<num>): The weighted term frequency vector.
    """
    ys = np.vectorize(lambda x: 1 if x else 0)(ws)
    return __normalize(ws, ys, normalize)

def __local_augmented(ws, normalize=False):
    """
    The augmented weight considers the maximally occurring term in each
    sentence and scales the weight of each word according to that.

    # Arguments

    * `ws` (numpy.array<num>): The term frequency vector.
    * `normalize` (bool): Indicates whether the result should be normalized.

    # Returns

    (numpy.array<num>): The weighted term frequency vector.
    """
    ys = 0.5 + 0.5 * (ws / np.max(ws))
    return __normalize(ws, ys, normalize)

def __local_logarithm(ws, normalize=False):
    """
    The logarithmic weight is simply logarithmically proportional to the
    unweighted term frequency.

    # Arguments

    * `ws` (numpy.array<num>): The term frequency vector.
    * `normalize` (bool): Indicates whether the result should be normalized.

    # Returns

    (numpy.array<num>): The weighted term frequency vector.
    """
    ys = np.log(1 + ws)
    return __normalize(ws, ys, normalize)

def __global_none(word_matrix):
    """
    The term weight is set to 1 for any term in the document.

    # Arguments

    * `word_matrix` (numpy.matrix<num>): A matrix representing the word
        frequency of a document, where the terms of the doucment are the rows
        in sorted order, and the columns are the sentences.

    # Returns

    (numpy.array<num>): A vector with the term weights for each term in the
    document in sorted order.
    """
    return np.ones(word_matrix.shape[0])

def __global_inverse(word_matrix):
    """
    The term weight is propertional to the log of the inverse fraction of
    sentences that contain the term.

    # Arguments

    * `word_matrix` (numpy.matrix<num>): A matrix representing the word
        frequency of a document, where the terms of the doucment are the rows
        in sorted order, and the columns are the sentences.

    # Returns

    (numpy.array<num>): A vector with the term weights for each term in the
    document in sorted order.
    """
    ys = np.ones(word_matrix.shape[0])
    n = word_matrix.shape[1] # The number of sentences
    for i in range(len(ys)):
        ni = np.count_nonzero(word_matrix[i,:])
        ys[i] = np.log(n / ni)
    return ys


# The local weight names that are allowed
LOCAL_WEIGHTS = {
    'none':      __local_none,
    'binary':    __local_binary,
    'augmented': __local_augmented,
    'logarithm': __local_logarithm,
}

# The global weight names that are allowed
GLOBAL_WEIGHTS = {
    'none':    __global_none,
    'inverse': __global_inverse,
}

def local_builder(name, normalize=False):
    """
    Build a local weighting function.

    # Arguments

    * `name` (str): The name of the weighting strategy to use.
    * `normalize` (bool): Indicates that the weights should be normalized.

    # Returns

    (func<a> -> a where a is numpy.array<num>): A function that takes a word
    frequency vector for a sentence and weights it, returning a new vector.
    """
    return lambda x: LOCAL_WEIGHTS[name.lower()](x, normalize)

def global_builder(name):
    """
    Build a global weighting function.

    # Arguments

    * `name` (str): The name of the weighting strategy to use.

    # Returns

    (func<a> -> a where a is numpy.array<num>): A function that takes a word
    matrix for a document and constructs a word frequency vector for a document
    for it.
    """
    return GLOBAL_WEIGHTS[name.lower()]
