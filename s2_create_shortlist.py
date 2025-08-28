import pandas as pd

# ----------------- USER CONFIG ----------------- #
input_csv = "gldv2_csvs/train.csv"             # original csv (has 'url' or 'filename' and 'landmark_id')
output_csv = "gldv2_csvs/cleaner_train.csv"    # resulting csv

# Inclusion lists:
# ranges inclusive: list of (start, end)
include_ranges = [(1, 25000)]
# individual landmark ids:
include_ids = []   # e.g. [101, 202, 303]

# thresholds
min_images_required = 50          # landmark must have >= this many images to be selected
max_images_keep_per_landmark = 70 # for selected landmarks, keep at most this many rows
max_unique_landmarks = 10        # cap number of unique landmark IDs included

# sampling / reproducibility
sample_method = "random"   # "random" or "first"
random_seed = 42

# allowed file extensions (lowercase check)
allowed_extensions = ('.jpg', '.jpeg')
# ------------------------------------------------ #

print("[INFO] Loading CSV:", input_csv)
df = pd.read_csv(input_csv)

# check columns
if 'landmark_id' not in df.columns:
    raise SystemExit("CSV must contain 'landmark_id' column.")
if 'url' in df.columns:
    path_col = 'url'
elif 'filename' in df.columns:
    path_col = 'filename'
else:
    raise SystemExit("CSV must contain either 'url' or 'filename' column for image paths.")

# normalize types
df['landmark_id'] = df['landmark_id'].astype(int)

# filter by extension
df[path_col] = df[path_col].astype(str)
df_filtered_ext = df[df[path_col].str.lower().str.endswith(allowed_extensions)].copy()
print(f"[INFO] Rows after extension filter ({', '.join(allowed_extensions)}): {len(df_filtered_ext)}")

# build requested id set from ranges + singles
requested_ids = []
for a, b in include_ranges:
    requested_ids.extend(range(a, b + 1))
requested_ids.extend(include_ids)

if not requested_ids:
    raise SystemExit("No landmark IDs specified in include_ranges or include_ids. Set at least one.")

print(f"[INFO] Total requested IDs (before filtering): {len(requested_ids)}")

# count images per landmark (after extension filter)
counts = df_filtered_ext['landmark_id'].value_counts()

# filter IDs that meet min threshold
valid_ids = [lid for lid in requested_ids if counts.get(lid, 0) >= min_images_required]

print(f"[INFO] IDs meeting min_images_required ({min_images_required}): {len(valid_ids)}")

# enforce max_unique_landmarks
if len(valid_ids) > max_unique_landmarks:
    valid_ids = valid_ids[:max_unique_landmarks]
    print(f"[INFO] Truncated to first {max_unique_landmarks} landmarks (due to max_unique_landmarks).")

print(f"[INFO] Final landmarks selected: {len(valid_ids)}")

# build output dataframe
selected_frames = []
for lid in valid_ids:
    rows = df_filtered_ext[df_filtered_ext['landmark_id'] == lid].copy()
    total_here = len(rows)
    keep_n = min(total_here, max_images_keep_per_landmark)
    if keep_n == 0:
        continue
    if sample_method == "random":
        sampled = rows.sample(n=keep_n, random_state=random_seed)
    else:
        sampled = rows.head(keep_n)
    sampled['_original_count'] = total_here
    sampled['_kept_count'] = keep_n
    selected_frames.append(sampled)

if not selected_frames:
    print("[WARN] No landmarks selected after applying filters.")
    result_df = pd.DataFrame(columns=df_filtered_ext.columns.tolist() + ['_original_count', '_kept_count'])
else:
    result_df = pd.concat(selected_frames, ignore_index=True)
    result_df = result_df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

# save
# drop helper columns before saving
cols_to_drop = ['_original_count', '_kept_count']
result_df = result_df.drop(columns=[c for c in cols_to_drop if c in result_df.columns])

result_df.to_csv(output_csv, index=False)
print(f"[INFO] Saved filtered csv to: {output_csv}")
print(f"[INFO] Total rows saved: {len(result_df)}")
print(f"[INFO] Unique landmarks saved: {result_df['landmark_id'].nunique()}")


# summary
if len(valid_ids) > 0:
    print("\n[INFO] Per-landmark kept counts (kept_count / original_count):")
    for lid in valid_ids:
        orig = counts.get(lid, 0)
        kept = min(orig, max_images_keep_per_landmark)
        print(f"  {lid}: {kept} / {orig}")

print("\n[INFO] Done.")
