#!/bin/sh

# pytest -k "$1" -v tests/tests.py

pytest -n 3 -k "$1" -v
