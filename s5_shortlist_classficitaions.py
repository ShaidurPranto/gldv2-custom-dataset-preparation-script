import pandas as pd

# Paths
csv1 = "gldv2_csvs/train_label_to_category.csv"   # has landmark_id,category
csv2 = "gldv2_dataset/gldv2_dataset.csv"                  # has filename,landmark_id
output_csv = "gldv2_dataset/filtered_train_label_to_category.csv"

# Load CSVs
df1 = pd.read_csv(csv1)   # landmark_id, category
df2 = pd.read_csv(csv2)   # filename, landmark_id

# Ensure landmark_id is same type
df1['landmark_id'] = df1['landmark_id'].astype(int)
df2['landmark_id'] = df2['landmark_id'].astype(int)

# Filter mapping (only keep IDs present in df2)
ids_in_train = df2['landmark_id'].unique()
filtered = df1[df1['landmark_id'].isin(ids_in_train)]

# Save
filtered.to_csv(output_csv, index=False)

print(f"✅ Saved {len(filtered)} rows to {output_csv}")
