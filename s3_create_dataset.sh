#!/bin/bash

# Input CSV file (the one you provided)
INPUT_CSV="gldv2_csvs/cleaner_train.csv"

# Directory variable for the dataset
DATASET_DIR="gldv2_dataset"

# Output CSV file
OUTPUT_CSV="gldv2_dataset.csv"

# Create dataset directory and images subfolder
mkdir -p "$DATASET_DIR/images"

echo "Starting image download..."

# Write header for output CSV
echo "filename,landmark_id" > "$DATASET_DIR/$OUTPUT_CSV"

# Read input CSV (skip header)
tail -n +2 "$INPUT_CSV" | while IFS=, read -r id url landmark_id; do
    # Get file extension from URL
    extension="${url##*.}"
    
    # Filename = id + extension
    filename="${id}.${extension}"
    
    # Download the image
    curl -s -L -o "$DATASET_DIR/images/$filename" "$url"
    
    # Append to output CSV
    echo "$filename,$landmark_id" >> "$DATASET_DIR/$OUTPUT_CSV"
    
    echo "Downloaded $filename"
done

echo "All images downloaded successfully into $DATASET_DIR/images"
echo "CSV mapping saved as $DATASET_DIR/$OUTPUT_CSV"
