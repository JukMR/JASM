#!/bin/bash

# Define the root directory from where the search should start
TARGET_DIRECTORY="tests/binary/shaXsum"

# Define main executable file
MAIN_EXECUTABLE="main.py"

# Define the command pattern
COMMAND_PATTERN="python3 $MAIN_EXECUTABLE --all-matches --return_addrs_and_instructions -p tests/yamls/arx.yaml -b"

# Find and process all files from the target directory
find "$TARGET_DIRECTORY" -type f \( -iname "*" \) -exec sh -c '
for file do
    echo "Processing $file..."
    '"$COMMAND_PATTERN"' "$file"
done
' sh {} +

echo "Executing individual tests..."
echo "-----------------------------"
FILE="zip.bin"
echo "Processing $FILE..."
python3 $MAIN_EXECUTABLE --all-matches --return_addrs_and_instructions -p tests/yamls/arx.yaml -b tests/binary/$FILE

FILE="md5sum"
echo "Processing $FILE..."
python3 $MAIN_EXECUTABLE --all-matches --return_addrs_and_instructions -p tests/yamls/arx.yaml -b tests/binary/md5sum

echo "Done."
