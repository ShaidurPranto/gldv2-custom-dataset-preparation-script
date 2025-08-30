# GLDv2 Dataset Preparation

After running the provided scripts, the following folders and files will be created:


## Folder Descriptions

- **`gldv2_csvs/`**  
  Contains CSV files related to metadata and filtering:
  - `train.csv` – Original GLDv2 metadata file.  
  - `train_label_to_category.csv` – Maps `landmark_id` to human-readable category.  
  - `cleaner_train.csv` – Filtered shortlist of images used for the dataset.  

- **`gldv2_dataset/`**  
  Contains the prepared dataset ready for training:
  - `images/` – Downloaded images corresponding to the shortlist.  
  - `gldv2_dataset.csv` – References local images with their metadata.  
  - `train.csv` – Training split.  
  - `val.csv` – Validation split.  
  - `test.csv` – Test split.  

---

✅ This structure ensures that metadata, images, and train/val/test splits are cleanly separated for easy experimentation.
