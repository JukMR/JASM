#!/bin/sh

set -eu

ARG_1=$1
shift

# pytest -k "$ARG_1" -v tests/tests.py

# Run integral tests

pytest -n 3 -k "$ARG_1" "$@"

# Run unit tests
# pytest -n 3 -k "$ARG_1" -v tests/unit_tests.py
