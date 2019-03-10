"""
This script performs summarization by applying the relevance measure.
"""

import argparse
import os

from utils import doc
from utils import fs

#------------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Summarize articles using the relevance measure.')
parser.add_argument('output_dir', type=str,
        help='The directory which to write the output data')
parser.add_argument('input_dir', type=str,
        help='The directory which contains the input data')
args = parser.parse_args()

# Get the command line arguments in a usable form
OUTPUT_DIR = os.path.abspath(args.output_dir)
INPUT_DIR  = os.path.abspath(args.input_dir)

# Create the ouput directory
fs.make_dir(OUTPUT_DIR)

#------------------------------------------------------------------------------
# Process the data
#------------------------------------------------------------------------------

INPUT_FILENAMES = sorted(fs.list_dir(INPUT_DIR, files=True))

# TODO Get these from the command line
# The weightings to use
LOCAL_WEIGHT  = lambda x: x
GLOBAL_WEIGHT = lambda x: x

for fname in INPUT_FILENAMES:
    input_file = os.path.join(INPUT_DIR, fname)
    output_file = os.path.join(OUTPUT_DIR, fname)
    # Prepare the file
    document = doc.Document.load_file(input_file)
    # The global document weight vector
    word_weights = document.word_weights(GLOBAL_WEIGHT)
    # The words in the file as a matrix
    word_matrix = document.word_matrix(LOCAL_WEIGHT)
    # Take the appropriate inner product for the sentences
    # TODO
    # Sort the sentences by maximum relevancy score
    # TODO
    # Determine the number of sentences to include in the summary
    # TODO
    # Pick the sentences for the summary
    # TODO
    # Write back the summary to the document
    # TODO
    document.dump_file(output_file)
