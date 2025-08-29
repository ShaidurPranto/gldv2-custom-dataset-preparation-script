import pandas as pd
import json

# -----------------------------
# Paths to your CSV files
# -----------------------------
train_csv_path = "gldv2_dataset/filtered_train_label_to_category.csv"
dataset_csv_path = "gldv2_dataset/gldv2_dataset.csv"

# -----------------------------
# Load CSVs
# -----------------------------
train_df = pd.read_csv(train_csv_path)
dataset_df = pd.read_csv(dataset_csv_path)

# -----------------------------
# Create contiguous mapping
# -----------------------------
# Combine all unique landmark_ids
all_landmark_ids = pd.concat([train_df['landmark_id'], dataset_df['landmark_id']]).unique()
all_landmark_ids.sort()  # optional: for consistent mapping

# Mapping: original landmark_id -> contiguous integer starting from 0
landmark_id_to_idx = {int(lid): int(idx) for idx, lid in enumerate(all_landmark_ids)}

# -----------------------------
# Apply mapping to CSVs
# -----------------------------
train_df['landmark_id'] = train_df['landmark_id'].map(landmark_id_to_idx)
dataset_df['landmark_id'] = dataset_df['landmark_id'].map(landmark_id_to_idx)

# -----------------------------
# Save CSVs in place
# -----------------------------
train_df.to_csv(train_csv_path, index=False)
dataset_df.to_csv(dataset_csv_path, index=False)

# -----------------------------
# Save mapping for reference
# -----------------------------
with open("landmark_id_mapping.json", "w") as f:
    json.dump(landmark_id_to_idx, f)

# -----------------------------
# Quick check
# -----------------------------
print("\nQuick check of first 10 rows of the updated CSVs:")
print("\nFiltered train label to category CSV:")
print(train_df.head(10))

print("\nDataset CSV:")
print(dataset_df.head(10))

print("\nTotal unique landmark_ids:", len(landmark_id_to_idx))
print("Mapping saved as 'landmark_id_mapping.json'.\n")
print("✅ CSVs updated successfully. You can now use 'landmark_id' directly for training.")
