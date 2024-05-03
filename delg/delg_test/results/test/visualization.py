import os
import argparse
from PIL import Image
import matplotlib.pyplot as plt

def extract_labels(matches_file):
    """ 提取所有不重复的标签 """
    labels = set()
    with open(matches_file, 'r') as file:
        for line in file:
            _, image2_name = line.strip().split(':')
            label = image2_name.strip().rpartition('_')[0]
            labels.add(label)
    return labels

def display_images_with_labels(data_directory, matches_file, max_rows=None):
    """ 显示图片对及其标签 """
    row_count = 0
    with open(matches_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if max_rows is not None and row_count >= max_rows:
            break

        image1_name, image2_name = line.strip().split(':')
        image1_name, image2_name = image1_name.strip(), image2_name.strip()

        label = image2_name.rpartition('_')[0]  # 提取标签

        image1_path = os.path.join(data_directory, image1_name + '.jpg')
        image2_path = os.path.join(data_directory, image2_name + '.jpg')
        
        try:
            image1 = Image.open(image1_path)
            image2 = Image.open(image2_path)

            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(image1)
            plt.title(f"{image1_name}\nLabel: {label}")
            plt.axis('off')

            plt.subplot(1, 2, 2)
            plt.imshow(image2)
            plt.title(f"{image2_name}\nLabel: {label}")
            plt.axis('off')

            plt.show()
            row_count += 1

        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue

def main():
    parser = argparse.ArgumentParser(description="Process images and extract labels.")
    parser.add_argument('--data_directory', type=str, required=True, help='Directory where images are stored')
    parser.add_argument('--matches_file', type=str, required=True, help='File containing matches')
    parser.add_argument('--output_file', type=str, required=True, help='File to save unique labels')
    parser.add_argument('--max_rows', type=int, help='Maximum number of rows to display', default=None)

    args = parser.parse_args()

    labels = extract_labels(args.matches_file)
    with open(args.output_file, 'w') as f:
        for label in sorted(labels):
            f.write(label + '\n')

    display_images_with_labels(args.data_directory, args.matches_file, args.max_rows)

    print(f"Labels have been extracted and saved to {args.output_file}.")

if __name__ == '__main__':
    main()
