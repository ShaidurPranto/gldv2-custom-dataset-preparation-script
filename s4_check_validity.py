from PIL import Image
import os

DATA_DIR = "./gldv2_dataset/images"

bad_files = []
for fname in os.listdir(DATA_DIR):
    if fname.lower().endswith((".jpg", ".jpeg", ".png")):
        try:
            img = Image.open(os.path.join(DATA_DIR, fname))
            img.verify()  # check file integrity
        except Exception as e:
            bad_files.append((fname, str(e)))

print(f"Checked {len(os.listdir(DATA_DIR))} files")
if bad_files:
    bad_files_count = 0
    print("Bad files found:")
    for bf in bad_files:
        bad_files_count += 1
        print(bf)
    print(f"Total bad files found: {bad_files_count} among {len(os.listdir(DATA_DIR))} checked files")
else:
    print("✅ All images are valid")
