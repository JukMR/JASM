#!/bin/sh

# This script is used to run tests with pytest

set -eu

# Initialize arguments for benchmark save and compare
BENCHMARK_SAVE=""
BENCHMARK_COMPARE=""

# Check for special benchmark arguments
while [ $# -gt 0 ]; do
    case "$1" in
    --benchmark-save)
        echo "Benchmark save: $2"
        BENCHMARK_SAVE="--benchmark-save=$2"
        ENABLE_BENCHMARK=true
        shift 2
        ;;
    --benchmark-compare)
        echo "Benchmark compare: $2"
        BENCHMARK_COMPARE="--benchmark-compare=$2"
        shift 2
        ENABLE_BENCHMARK=true
        ;;
    *)
        break
        ;;
    esac
done

# Check if there is at least one argument left for -k option
if [ $# -eq 0 ]; then
    echo "No test selection argument provided"
    ARG_1=""
else
    ARG_1="-k $1"
    shift
fi

# Configure PYTHONPATH
if [ -z "${PYTHONPATH:-}" ]; then
    export PYTHONPATH="."
else
    export PYTHONPATH="$PYTHONPATH:."
fi

# Check whetever ENABLE_BENCHMARK is set
if [ -n "${ENABLE_BENCHMARK:-}" ]; then
    echo "Running tests with benchmarking"
    pytest -vv --fail-slow 5s --enable-benchmark "$BENCHMARK_SAVE" "$BENCHMARK_COMPARE" "$ARG_1" "$@"

else
    echo "Running tests without benchmarking"
    pytest -vv --fail-slow 5s "$ARG_1" "$@"

fi
