import pandas as pd
import json

def filter_landmarks(images_csv, categories_csv, threshold, output_file):
    # Read CSVs
    df_images = pd.read_csv(images_csv)
    df_categories = pd.read_csv(categories_csv)

    # Keep only valid .jpg urls (case-insensitive)
    df_images = df_images[df_images['url'].str.lower().str.endswith('.jpg')]

    # Count images per landmark_id
    counts = df_images.groupby('landmark_id').size().reset_index(name='count')

    # Filter by threshold
    valid_ids = counts[counts['count'] >= threshold]['landmark_id'].tolist()

    # Get categories for valid_ids
    categories = df_categories[df_categories['landmark_id'].isin(valid_ids)]
    categories_dict = dict(zip(categories['landmark_id'], categories['category']))

    # Prepare result
    result = {
        "valid_landmark_ids": valid_ids,
        "landmark_categories": categories_dict
    }

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"✅ Output saved to {output_file}")


# Example usage
if __name__ == "__main__":
    filter_landmarks(
        "./gldv2_csvs/train.csv",
        "./gldv2_csvs/train_label_to_category.csv",
        threshold=510,
        output_file="shortlist.json"
    )
