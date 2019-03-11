
"""
This script performs summarization by latent semantic analysis.
"""

import argparse
import json
import os

from utils import doc
from utils import fs

#------------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Summarize articles using the latent semantic analysis.')
parser.add_argument('output_file', type=str,
        help='The file which to write the output data')
parser.add_argument('input_dir', type=str,
        help='The directory which contains the input data')
args = parser.parse_args()

# Get the command line arguments in a usable form
OUTPUT_FILE = os.path.abspath(args.output_file)
INPUT_DIR   = os.path.abspath(args.input_dir)

# Create the ouput directory
fs.make_dir(os.path.dirname(OUTPUT_FILE))

#------------------------------------------------------------------------------
# Process the data
#------------------------------------------------------------------------------

RESULTS = []

def evaluate(strategy, fname):
    """
    TODO Docs
    """
    document = doc.Document.load_file(fname)
    # Make sure that every sentence in the summary is also in the article
    for sentence in document.sent_gen_summary:
        if sentence not in document.sent_orig_article:
            print(f"Summary for {clr.blu(document.title)} has the sentence:")
            print(f"    {clr.red(sentence)}")
            print(f"which does not appear in article.")
            print()
    # Compute the precision, recall, and f-score
    sgs = set(document.sent_gen_summary)
    sos = set(document.sent_orig_summary)
    p = len(sos & sgs) / len(sos)
    r = len(sos & sgs) / len(sgs)
    f = (2 * r * p) / (r + p) if r != 0 and p != 0 else 0 # Prevent divide by 0
    return {
        'f': f,
        'file': fname,
        'p': p,
        'r': r,
        'strategy': strategy,
        'topic': document.topic,
    }

# The directories with results to iterate over
INPUT_SUBDIRS = sorted(fs.list_dir(INPUT_DIR, dirs=True, full=True))

# Compute the results
RESULTS = []
for dir in INPUT_SUBDIRS:
    INPUT_FILENAMES = sorted(fs.list_dir(dir, files=True, full=True))
    strategy = os.path.basename(dir)
    for fname in INPUT_FILENAMES:
        input_file = os.path.join(INPUT_DIR, fname)
        result = evaluate(strategy, input_file)
        RESULTS.append(result)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(RESULTS, f, indent=2, sort_keys=True)
