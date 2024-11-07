#!/bin/bash

DIRECTORY_NAME="__pycache__"
echo "Removing all directories named '$DIRECTORY_NAME' recursively"

echo "Are you sure you want to continue"
select yn in "Yes" "No"; do
    case $yn in
    Yes) break ;;
    No) exit ;;
    esac
done

echo 'Removing all directories named '$DIRECTORY_NAME' recursively'
find . -type d -name "$DIRECTORY_NAME" -exec rm -rfv {} \;
