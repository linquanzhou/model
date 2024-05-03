import os

def generate_index_list(root_dir, output_file):
    with open(output_file, 'w') as file:
        for subdir, dirs, files in os.walk(root_dir):
            for file_name in files:
                if file_name.endswith('.jpg'):  # Ensure we're only processing .jpg files
                    # Remove the .jpg extension from the file path
                    file_path = os.path.join(subdir, file_name[:-4])
                    file.write(file_path + '\n')

root_directory = '/Users/zz/Desktop/models/research/delf/delf/python/delg/delg_test/data/gld_index'
output_index_list = '/Users/zz/Desktop/models/research/delf/delf/python/delg/delg_test/gld_index_list.txt'
generate_index_list(root_directory, output_index_list)
