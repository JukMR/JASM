#!/bin/bash

echo "Running mypy on all Python files in the current directory"
mypy --strict \
    --disallow-incomplete-defs \
    --disallow-untyped-calls \
    --disallow-untyped-defs \
    --no-implicit-optional \
    --show-error-codes \
    --strict-equality \
    --warn-redundant-casts \
    --warn-unreachable \
    --warn-unused-configs \
    --warn-unused-ignores \
    --follow-imports=skip \
    src/
