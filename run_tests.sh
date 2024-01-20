#!/bin/sh

# pytest -k "$1" -v tests/tests.py

# Run integral tests
pytest -n 3 -k "$1" -v

# Run unit tests
# pytest -n 3 -k "$1" -v tests/unit_tests.py
