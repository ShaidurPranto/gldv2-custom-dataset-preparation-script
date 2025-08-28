Resulting folders and files (after running the scripts)
gldv2_csvs/
├─ train.csv                    # GLDv2 original metadata (id, url, landmark_id, ...)
├─ train_label_to_category.csv  # landmark_id -> human-readable category
└─ cleaner_train.csv            # filtered shortlist (id, url, landmark_id)

gldv2_dataset/
├─ images/                      # downloaded images for the shortlist
├─ gldv2_dataset.csv            # final dataset referencing local files
├─ train.csv                    # split: training rows
├─ val.csv                      # split: validation rows
└─ test.csv                     # split: test rows
