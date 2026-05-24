#!/bin/bash

FOLDER=${1:-.}

find "$FOLDER" -mindepth 1 -maxdepth 2 -type d | while read -r subfolder; do
    echo "Processing folder: $subfolder"
    count=0

    for file in "$subfolder"/*.pdf "$subfolder"/*.docx; do
        [ -f "$file" ] || continue
        [ $count -ge 4 ] && break

        echo "Uploading $file..."
        curl -X POST "http://localhost:8000/api/candidate/upload-cv" \
             -H "accept: application/json" \
             -F "files=@$file"

        ((count++))
    done
done