#!/bin/sh

set -eu
# Check if there is at least one argument
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    ARG_1=""
else
    ARG_1="-k $1"
    shift
fi

# Export current directory to PYTHONPATH so pytest can see the files

# Check if PYTHONPATH is empty
if [ -z "${PYTHONPATH:-}" ]; then
    # If empty, set it to current directory
    export PYTHONPATH="."
else
    # If not empty, append current directory to it
    export PYTHONPATH="$PYTHONPATH:."
fi

# pytest -k "$ARG_1" -v tests/tests.py

# Run integral tests
pytest -n 4 -v "$ARG_1" "$@"

# Make sure capture groups sequencial tests are working!
if [ "$(pytest -k capture_group -n 1 | grep -c FAILED)" = 3 ]; then
    echo "Some capture group tests start failing again!"
else
    echo "Capture test passed!"
    exit 0
fi
