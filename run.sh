#!/usr/bin/env sh

# This script runs all of the programs automatically

# The relative directories where everything is stored.
CORPUS_DIR=corpus/
PREP_DIR=prep/
REL_DIR=rel/
LSM_DIR=lsm/

# These are the command line arguments.
CLEAN=0
HELP=0

for i in "$@"; do
    case $i in
        --clean)
        CLEAN=1
        ;;
        --help)
        HELP=1
        ;;
        *)
        echo "Bad argument '$i'. Run with --help."
        exit 1
        ;;
    esac
done

if [ "$HELP" -eq "1" ]; then
    echo "Run all of the scripts in this project sequentially:"
    echo "  - preprocess.py"
    echo "  - relevance_measure.py"
    echo ""
    echo "The following arguments are allowed:"
    echo "  --clean   Remove all generated data."
    echo "  --help    Show this information."
elif [ "$CLEAN" -eq "1" ]; then
    rm -rf $PREP_DIR
    rm -rf $REL_DIR
    rm -rf $LSM_DIR
else
    python3 prep.py $PREP_DIR $CORPUS_DIR
    python3 rel.py $REL_DIR $PREP_DIR
    python3 lsm.py $LSM_DIR $PREP_DIR
fi
