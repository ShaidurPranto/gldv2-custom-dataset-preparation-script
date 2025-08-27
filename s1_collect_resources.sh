#!/bin/bash

# Script to download Google Landmark metadata CSV files into a specified folder

# Folder name variable
DOWNLOAD_DIR="gldv2_csvs"

echo "Starting download of Google Landmark metadata files into folder: $DOWNLOAD_DIR"

# Create folder if it doesn't exist
mkdir -p "$DOWNLOAD_DIR"

# Change to the folder
cd "$DOWNLOAD_DIR" || { echo "Failed to enter directory $DOWNLOAD_DIR"; exit 1; }

# Download the files
curl -O https://s3.amazonaws.com/google-landmark/metadata/train.csv
# curl -O https://s3.amazonaws.com/google-landmark/metadata/train_clean.csv
# curl -O https://s3.amazonaws.com/google-landmark/metadata/train_attribution.csv
curl -O https://s3.amazonaws.com/google-landmark/metadata/train_label_to_category.csv
# curl -O https://s3.amazonaws.com/google-landmark/metadata/train_label_to_hierarchical.csv

echo "All files downloaded successfully into $DOWNLOAD_DIR!"
