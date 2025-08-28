import pandas as pd
from sklearn.model_selection import train_test_split

# ---------------- CONFIG ---------------- #
input_csv = "gldv2_dataset/gldv2_dataset.csv"
train_csv = "gldv2_dataset/train.csv"
val_csv   = "gldv2_dataset/val.csv"
test_csv  = "gldv2_dataset/test.csv"

# proportions (must sum to 1.0)
train_size = 0.7
val_size   = 0.15
test_size  = 0.15

random_seed = 42
# ---------------------------------------- #

print("[INFO] Loading dataset:", input_csv)
df = pd.read_csv(input_csv)

# sanity check
if not {"filename", "landmark_id"}.issubset(df.columns):
    raise SystemExit("CSV must contain 'filename' and 'landmark_id' columns.")

# first split: train vs (val+test)
df_train, df_temp = train_test_split(
    df,
    train_size=train_size,
    stratify=df["landmark_id"],  # stratify to preserve class distribution
    random_state=random_seed
)

# adjust val/test ratio relative to df_temp
val_ratio = val_size / (val_size + test_size)

df_val, df_test = train_test_split(
    df_temp,
    train_size=val_ratio,
    stratify=df_temp["landmark_id"],
    random_state=random_seed
)

# save splits
df_train.to_csv(train_csv, index=False)
df_val.to_csv(val_csv, index=False)
df_test.to_csv(test_csv, index=False)

print(f"[INFO] Train: {len(df_train)} rows -> {train_csv}")
print(f"[INFO] Val:   {len(df_val)} rows -> {val_csv}")
print(f"[INFO] Test:  {len(df_test)} rows -> {test_csv}")
print(f"[INFO] Unique landmarks: Train={df_train['landmark_id'].nunique()}, "
      f"Val={df_val['landmark_id'].nunique()}, Test={df_test['landmark_id'].nunique()}")
