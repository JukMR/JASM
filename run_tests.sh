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

# Append current directory to PYTHONPATH
PYTHONPATH=$PYTHONPATH:.
export PYTHONPATH="$PYTHONPATH"
# pytest -k "$ARG_1" -v tests/tests.py

# Run integral tests
pytest -n 3 -v "$ARG_1" "$@"

# Run unit tests
# pytest -n 3 -k "$ARG_1" -v tests/unit_tests.py
