#!/bin/bash

SRC_DIR="src"
TESTS_DIR="tests/unit_tests"

# Create the base directory for unit tests if it doesn't exist
mkdir -p $TESTS_DIR

# Loop over each file in the src directory
find $SRC_DIR -name '*.py' | while read -r fname; do
    # Replace the src directory with the tests directory in the file path
    TEST_PATH=${fname/$SRC_DIR/$TESTS_DIR}

    # Create the directory structure in the tests directory
    mkdir -p "$(dirname "$TEST_PATH")"

    # Replace the .py extension with _test.py for the test file
    TEST_FILE="$(dirname "$TEST_PATH")/test_$(basename "$TEST_PATH")"

    # Create an empty test file if it doesn't exist
    [ -f "$TEST_FILE" ] || touch "$TEST_FILE"
done

echo "Unit test structure created under $TESTS_DIR"
