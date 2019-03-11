#!/usr/bin/env python3

"""
This script runs all of the programs in the project in the correct order to
produce a result.
"""

import argparse
import itertools
import shutil
import subprocess
import os

from utils import color as clr

# The relative directories where everything is stored.
CORPUS_DIR = os.path.abspath("corpus")
EVAL_DIR   = os.path.abspath("eval")
SUMM_DIR   = os.path.abspath("summary")
PREP_DIR   = os.path.abspath("prep")

# The names of programs
EVAL_NAME = "eval"
LSA_NAME  = "lsa"
PREP_NAME = "prep"
REL_NAME  = "rel"

# The names of weighting options
GLOBAL_WEIGHTS = ["none", "inverse"]
LOCAL_WEIGHTS  = ["none", "binary", "augmented", "logarithm"]
NORMALIZATIONS = ["false", "true"]

# Parse the command line arguments
parser = argparse.ArgumentParser(
        description='Run the program.')
parser.add_argument('--clean', action='store_true',
        help="Clean all files.")
parser.add_argument('--eval', action='store_true',
        help="Run the evaluation.")
parser.add_argument('--prep', action='store_true',
        help="Run the preparation.")
parser.add_argument('--summarize', action='store_true',
        help="Run the summarization.")
args = parser.parse_args()

def run_cmd(cmd):
    """
    Run a command.

    # Arguments

    * `cmd` (list<str>): A list containing a command and its arguments.
    """
    print(f"{clr.cyn('RUNNING')} {' '.join(cmd)}")
    subprocess.call(cmd)

def run_clean():
    """
    Clean the program outputs.
    """
    def rmdirectory(path):
        print(f"{clr.cyn('DELETING')} {path}")
        shutil.rmtree(path, ignore_errors=True)
    rmdirectory(EVAL_DIR)
    rmdirectory(PREP_DIR)
    rmdirectory(SUMM_DIR)

def run_prep():
    """
    Run the preparation program.
    """
    run_cmd(['python3', f'{PREP_NAME}.py', PREP_DIR, CORPUS_DIR])

def run_lsa():
    """
    Run the latent semantic analysis program.
    """
    for lw, norm in itertools.product(LOCAL_WEIGHTS, NORMALIZATIONS):
        outdir=os.path.join(SUMM_DIR, f"{LSA_NAME}-{lw}-{norm}")
        run_cmd(['python3', f'{LSA_NAME}.py', outdir, PREP_DIR, lw, norm])

def run_rel():
    """
    Run the relevance measure program.
    """
    for lw, norm, gw in \
            itertools.product(LOCAL_WEIGHTS, NORMALIZATIONS, GLOBAL_WEIGHTS):
        outdir=os.path.join(SUMM_DIR, f"{REL_NAME}-{lw}-{norm}-{gw}")
        run_cmd(['python3', f'{REL_NAME}.py', outdir, PREP_DIR, lw, norm, gw])

def run_eval():
    """
    Run the evaluation program.
    """
    outfile = os.path.join(EVAL_DIR, f"{EVAL_NAME}.json")
    run_cmd(['python3', f'{EVAL_NAME}.py', outfile, SUMM_DIR])


if args.clean:
    run_clean()
else:
    # If no areguments are given then run everything, otherwise only run
    # specific parts
    RUN_PREP = args.prep
    RUN_SUMM = args.summarize
    RUN_EVAL = args.eval
    if not any([RUN_PREP, RUN_SUMM, RUN_EVAL]):
        RUN_PREP = True
        RUN_SUMM = True
        RUN_EVAL = True
    if RUN_PREP:
        run_prep()
    if RUN_SUMM:
        run_lsa()
        run_rel()
    if RUN_EVAL:
        run_eval()
