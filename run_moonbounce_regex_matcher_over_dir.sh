#!/bin/bash

# Define the root directory from where the search should start
ROOT_DIRECTORY="$HOME/eclypsium/cdt/binary-samples/uefi"

# Define main executable file
MAIN_EXECUTABLE="main.py"

# Define the command pattern
COMMAND_PATTERN="python3 $MAIN_EXECUTABLE --all-matches -p tests/yamls/moonbounce_regex_matcher.yaml -b"

# Find and process .efi and .bin files recursively
find "$ROOT_DIRECTORY" -type f \( -iname "*.efi" -o -iname "*.bin" \) -exec sh -c '
for file do
    echo "Processing $file..."
    '"$COMMAND_PATTERN"' "$file"
done
' sh {} +
