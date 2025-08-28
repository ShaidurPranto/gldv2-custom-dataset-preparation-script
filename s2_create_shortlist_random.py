import pandas as pd

# -------- User Config -------- #
train_csv = "gldv2_csvs/train.csv"          # Original GLDv2 train CSV
clean_train_csv = "gldv2_csvs/cleaner_train.csv"
num_landmarks = 10                         # Number of unique landmarks to keep
max_images_per_landmark = 50               # Upper threshold for images per landmark
# --------------------------- #

# Load the full train.csv
print("[INFO] Loading train.csv ...")
train_df = pd.read_csv(train_csv)

# Filter only rows with .jpg URLs
train_df = train_df[train_df['url'].str.lower().str.endswith('.jpg')]
print(f"[INFO] Filtered train.csv to only include .jpg images → {len(train_df)} rows remain")

# Count images per landmark
landmark_counts = train_df['landmark_id'].value_counts()

# Select top N landmark_ids with most images
top_landmarks = landmark_counts.head(num_landmarks).index.tolist()
print(f"[INFO] Selected top {num_landmarks} landmarks with most images.\n")

# Show how many images each selected landmark has
print("[INFO] Image counts per selected landmark_id (before capping):")
for lid in top_landmarks:
    count = landmark_counts[lid]
    print(f"  Landmark ID {lid}: {count} images")

# Filter train_df to keep only rows with top landmark_ids
filtered_df = train_df[train_df['landmark_id'].isin(top_landmarks)]

# Apply upper threshold per landmark
clean_train_df = filtered_df.groupby('landmark_id').head(max_images_per_landmark).reset_index(drop=True)

# Save cleaner_train.csv
clean_train_df.to_csv(clean_train_csv, index=False)
print(f"\n[INFO] cleaner_train.csv saved → {clean_train_csv}")
print(f"[INFO] Total rows in cleaner_train.csv: {len(clean_train_df)}")
print(f"[INFO] Number of unique landmarks: {clean_train_df['landmark_id'].nunique()}")

# Show counts after applying threshold
print("\n[INFO] Image counts per selected landmark_id (after capping):")
print(clean_train_df['landmark_id'].value_counts())
