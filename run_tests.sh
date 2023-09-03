#!/bin/sh

cd test && pytest -k "$1" -v tests.py
