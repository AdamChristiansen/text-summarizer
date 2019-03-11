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
OUT_DIR    = os.path.abspath("output")
PREP_DIR   = os.path.abspath("prep")

# The names of programs
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
parser.add_argument('--all', action='store_true',
        help="Run all configurations.")
parser.add_argument('--clean', action='store_true',
        help="Clean all files.")
args = parser.parse_args()

def run_cmd(cmd):
    """
    Run a command.

    # Arguments

    * `cmd` (list<str>): A list containing a command and its arguments.
    """
    print(f"{clr.yel('RUNNING')} {' '.join(cmd)}")
    subprocess.call(cmd)

def clean():
    """
    Clean the program outputs.
    """
    def rmdirectory(path):
        print(f"{clr.yel('DELETING')} {path}")
        shutil.rmtree(path, ignore_errors=True)
    rmdirectory(PREP_DIR)
    rmdirectory(OUT_DIR)

def prep():
    """
    Run the preparation program.
    """
    run_cmd(['python3', f'{PREP_NAME}.py', PREP_DIR, CORPUS_DIR])

def lsa():
    """
    Run the latent semantic analysis program.
    """
    outdir=os.path.join(OUT_DIR, LSA_NAME)
    run_cmd(['python3', f'{LSA_NAME}.py', outdir, PREP_DIR])

def rel():
    """
    Run the relevance measure program.
    """
    for lw, norm, gw in \
            itertools.product(LOCAL_WEIGHTS, NORMALIZATIONS, GLOBAL_WEIGHTS):
        outdir=os.path.join(OUT_DIR, f"{REL_NAME}-{lw}-{norm}-{gw}")
        run_cmd(['python3', f'{REL_NAME}.py', outdir, PREP_DIR, lw, norm, gw])
        if not args.all:
            break

if args.clean:
    clean()
else:
    prep()
    lsa()
    rel()
