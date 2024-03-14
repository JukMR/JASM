#!/bin/bash

# This script is used to run tests with pytest

set -eu

DISABLE_BENCHMARK=false

# Check for special benchmark arguments
while [ $# -gt 0 ]; do
    case "$1" in
    --disable-benchmark)
        echo "Disabling benchmark"
        DISABLE_BENCHMARK=true
        shift 1
        ;;
    *)
        break
        ;;
    esac
done

# Configure PYTHONPATH
if [ -z "${PYTHONPATH:-}" ]; then
    export PYTHONPATH="."
else
    export PYTHONPATH="$PYTHONPATH:."
fi

# Check whetever ENABLE_BENCHMARK is set

if [ "$DISABLE_BENCHMARK" == true ]; then
    echo "Running tests without benchmarking"
    pytest -vv --fail-slow 5s "$@"

else
    echo "Running tests with benchmarking"
    pytest -vv --fail-slow 15s --ignore-glob='*benchmark*degradation*' --enable-benchmark --benchmark-compare='benchmark_baseline/baseline.json' "$@"

fi
