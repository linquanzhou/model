import pandas as pd
import urllib.parse


def load_data(best_matches_file, index_to_id_file, label_to_url_file):
    with open(best_matches_file, 'r') as file:
        best_matches_data = file.read().splitlines()
    image_ids = [line.split('/')[-1] for line in best_matches_data]
    index_to_id = pd.read_csv(index_to_id_file)
    label_to_url = pd.read_csv(label_to_url_file)
    results = []
    for image_id in image_ids:
        match_id = index_to_id[index_to_id['id'] == image_id]
        if not match_id.empty:
            landmark_id = match_id['landmark_id'].iloc[0]
            match_url = label_to_url[label_to_url['landmark_id'] == landmark_id]
            if not match_url.empty:
                url = match_url['category'].iloc[0]
                parsed_url = urllib.parse.unquote(url)
                category_name = parsed_url.split('/')[-1].replace('_', ' ').replace('Category:', '')
                results.append((image_id, category_name.strip()))
    
    return results

best_matches_file = 'best_matches.txt'
index_to_id_file = 'index_image_to_landmark.csv'
label_to_url_file = 'index_label_to_category.csv'
results = load_data(best_matches_file, index_to_id_file, label_to_url_file)

# 输出结果
for result in results:
    print(f"Image ID: {result[0]}, Category: {result[1]}")
