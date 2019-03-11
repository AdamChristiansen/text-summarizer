"""
This script performs summarization by applying the relevance measure.
"""

import argparse
import os

import numpy as np

from utils import doc
from utils import fs
from utils import weight

#------------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Summarize articles using the relevance measure.')
parser.add_argument('output_dir', type=str,
        help='The directory which to write the output data')
parser.add_argument('input_dir', type=str,
        help='The directory which contains the input data')
parser.add_argument('local_weight', type=str,
        help='The local weighting strategy to use')
parser.add_argument('normalize', type=bool,
        help='Indicates the local weights should be normalized')
parser.add_argument('global_weight', type=str,
        help='The global weighting strategy to use')
args = parser.parse_args()

# Get the command line arguments in a usable form
OUTPUT_DIR = os.path.abspath(args.output_dir)
INPUT_DIR  = os.path.abspath(args.input_dir)
LOCAL_WEIGHT  = weight.local_builder(args.local_weight, args.normalize)
GLOBAL_WEIGHT = weight.global_builder(args.global_weight)

# Create the ouput directory
fs.make_dir(OUTPUT_DIR)

#------------------------------------------------------------------------------
# Process the data
#------------------------------------------------------------------------------

INPUT_FILENAMES = sorted(fs.list_dir(INPUT_DIR, files=True))

def summarize(document):
    """
    Generate a summary for a document and set it in place.

    # Arguments

    * `document (Document): The cocument to summarize.
    """
    # The global document weight vector and words in the file as a matrix
    weights = document.word_weights(GLOBAL_WEIGHT)
    matrix = document.word_matrix(LOCAL_WEIGHT)

    summary_indices = []
    for n in range(document.summary_size()):
        # Find the highest ranking sentence by iterating over the matrix
        # columns (sentences) and computing a ranking. The index of the highest
        # ranking sentence is chosen.
        max_index = None
        max_rank  = None
        for i in range(matrix.shape[1]):
            rank = np.dot(weights, matrix[:,i])
            if max_index is None or rank > max_rank:
                max_index = i
                max_rank  = rank
        # Select the highest ranking sentence
        summary_indices.append(max_index)
        # Remove all occurrences of words in the selected sentence from all
        # other sentences. This is done by iterating over the rows of the
        # matrix, and if the selected sentence is non-zero in that row,
        # set the entire row to 0.
        for i in range(matrix.shape[0]):
            if matrix[i, max_index]:
                matrix[i,:] = 0
    # Set the summary in the document
    print(summary_indices)
    document.set_summary(summary_indices)

for fname in INPUT_FILENAMES:
    input_file = os.path.join(INPUT_DIR, fname)
    output_file = os.path.join(OUTPUT_DIR, fname)
    # Prepare the file
    document = doc.Document.load_file(input_file)
    # Summarize the document in place
    summarize(document)
    # Write the generated document to the output location
    document.dump_file(output_file)
