
"""
This script performs summarization by latent semantic analysis.
"""

import argparse
import collections
import json
import os

import matplotlib.pyplot as plt
import numpy as np

from utils import color as clr
from utils import doc
from utils import fs

# Configure plots
plt.rcParams["font.size"]   = 11
plt.rcParams["text.usetex"] = True
plt.rcParams['figure.figsize'] = 5, 2.5

#------------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Summarize articles using the latent semantic analysis.')
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

RESULTS = []

def evaluate(fname, strategy):
    """
    Evaluate the results for a single summary.

    # Arguments

    * `fname` (str): The path to the summary file to evaluate.
    * `strategy` (str): A description of the summarization strategy.

    # Returns

    (dict<str, object>): The evaluation results.
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
        'strategy': document.summary_strategy,
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
        result = evaluate(input_file, strategy)
        RESULTS.append(result)

with open(os.path.join(OUTPUT_DIR, "results.json"), 'w') as f:
    json.dump(RESULTS, f, indent=2, sort_keys=True)

#------------------------------------------------------------------------------
# Interpret Results
#------------------------------------------------------------------------------

def print_heading(name):
    """
    Print a pretty section heading.

    # Arguments

    * `name` (str): The name of the section heading.
    """
    print()
    print(clr.blu(name))
    print(clr.blu(len(name) * '='))

def print_entry(e):
    """
    Print a pretty entry, where an entry is considered the result of evaluation
    of a single summary.

    # Arguments

    * `e` (dict): The entry.
    """
    print("strat={:10} topic={:14} doc={:25} p={:5.3f} r={:5.3f} f={:5.3f}"
        .format(e['strategy'], e['topic'], os.path.basename(e['file']), e['p'],
            e['r'], e['f']))

def print_pair(kn, kv, vn, vv, kw='20', vw='5.3f'):
    """
    Print a key-value pair.

    # Arguments

    * `kn` (obj): The key name.
    * `kv` (obj): The key value.
    * `vn` (obj): The value name.
    * `vv` (obj): The value value.
    * `kw` (str): The key value format specifier.
    * `vw` (str): The value value format specifier.
    """
    fmt = f"{{}}={{:{kw}}} {{}}={{:{vw}}}"
    print(fmt.format(kn, kv, vn, vv))

def group_reduce(f_agg, f_red, xs):
    """
    Group by a function and then reducethe groups.

    # Arguments

    * `f_agg` (func<obj> -> obj): A function which produces the key to group
        by.
    * `f_red` (func<list<obj>> -> obj): A function which is used to reduce a
        list. Note that the whole list is given, not just an `f(a, b) -> a`
        function for a generic reduce routine.
    * `xs` (list<obj>): The list of items to reduce.

    # Returns

    (dict<obj, obj>): A dictionary whose keys are the keys that are grouped on
    and the items are the reduced list of objects for each key.
    """
    # Aggregate by the aggregation function
    agg = collections.defaultdict(list)
    for x in xs:
        agg[f_agg(x)].append(x)
    # Reduce each aggregation
    r = {}
    for k, vs in agg.items():
        r[k] = f_red(vs)
    return r

def plot_results(filename, xs, ys, bottom=0, plot_func=plt.bar,
        rotate_label=False, title=None, xlabel=None, ylabel=None):
    """
    Create a plot of the results and save it to a file.

    # Arguments

    * `filename` (str): The file to save the plot to.
    * `xs` (list_like<obj>): The x data.
    * `ys` (list_like<obj>): The y data.
    * `bottom` (float): The relative offset for the bottom of the plot.
    * `plot_func` (func<a, a> where a is list_like<obj>): A function that
        series of x and y data, respectively, and creates a plot.
    * `rotate_labels` (bool): Indicates that the x labels should be rotated 90
        degrees.
    * `title` (None|str): The plot title, if specified.
    * `xlabel` (None|str): The x label title, if specified.
    * `ylabel` (None|str): The y label title, if specified.
    """
    plt.clf()
    plot_func(xs, ys)
    plt.subplots_adjust(bottom=bottom)
    if rotate_label:
        plt.xticks(xs, xs, rotation=90)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=600)

def results_by_strategy():
    """
    Report the results of different strategies.
    """
    results = group_reduce(lambda x: x['strategy'], lambda xs: np.mean(list(map(lambda x: x['f'], xs))), RESULTS)
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    print_heading("Strategy Ranking")
    strategies, fs = [], []
    for strategy, f in results:
        print_pair("strat", strategy, "f", f)
        strategies.append(strategy)
        fs.append(f)
    strategies = list(map(lambda s: f"$\\mathrm{{{s}}}$", strategies))
    plot_results('strategy.png', strategies, fs, bottom=0.35,
        rotate_label=True, xlabel="Configuration", ylabel="$F$")

def results_by_topic():
    """
    Report the results of summarizing different topics.
    """
    results = group_reduce(lambda x: x['topic'], lambda xs: np.mean(list(map(lambda x: x['f'], xs))), RESULTS)
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    print_heading("Topic Ranking")
    topics, fs = [], []
    for topic, f in results:
        print_pair("topic", topic, "f", f)
        topics.append(topic)
        fs.append(f)
    plot_results('topic.png', topics, fs, bottom=0.20, xlabel="Topic",
        ylabel="$F$")

def results_best_worst_individual(key=lambda x: x['f'], size=5):
    """
    Display the best and worst individual results from a single summarization.

    # Arguments

    * `key` (func<dict> -> obj): A function which selects a key in an entry to
        sort by.
    * `size` (int): The number of the best and worst results to show.
    """
    s = sorted(RESULTS, key=key, reverse=True)
    best = s[0:size]
    worst = s[-size:]
    print_heading("Best Individual")
    for e in best:
        print_entry(e)
    print_heading("Worst Individual")
    for e in worst:
        print_entry(e)
    # Create a histogram of the results
    fs = []
    for r in s:
        fs.append(r['f'])
    plot_results('individual.png', None, fs, bottom=0.20,
        plot_func=lambda xs, ys: plt.hist(ys, bins=20), xlabel="$F$", ylabel="Count")

# Run all of the procedures
results_by_strategy()
results_by_topic()
results_best_worst_individual()
