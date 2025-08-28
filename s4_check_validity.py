from PIL import Image
import os
import pandas as pd

DATA_DIR = "./gldv2_dataset/images"
DATASET_CSV = "./gldv2_dataset/gldv2_dataset.csv"

# Load the dataset CSV
df = pd.read_csv(DATASET_CSV)

bad_files = []

# Iterate over image files
for fname in os.listdir(DATA_DIR):
    if fname.lower().endswith((".jpg", ".jpeg", ".png")):
        file_path = os.path.join(DATA_DIR, fname)
        try:
            img = Image.open(file_path)
            img.verify()  # check file integrity
        except Exception as e:
            bad_files.append((fname, str(e)))
            # Delete the invalid image file
            os.remove(file_path)
            # Remove the corresponding row from CSV dataframe
            df = df[df['filename'] != fname]

# Save the updated CSV
df.to_csv(DATASET_CSV, index=False)

print(f"Checked {len(os.listdir(DATA_DIR)) + len(bad_files)} files")
if bad_files:
    print("Bad files found and removed:")
    for bf in bad_files:
        print(bf)
    print(f"Total bad files removed: {len(bad_files)}")
else:
    print("✅ All images are valid")

# Count number of valid images per landmark_id
landmark_counts = df['landmark_id'].value_counts().sort_index()
print("\nNumber of valid images per landmark_id:")
for landmark_id, count in landmark_counts.items():
    print(f"Landmark {landmark_id}: {count} images")
