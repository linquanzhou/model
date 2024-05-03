from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import time
import numpy as np
import tensorflow as tf
from absl import app, flags
from delf import datum_io
from delf import feature_io
from delf import extractor
from delf import utils

flags.DEFINE_string('delf_config_path', '/tmp/delf_config_example.pbtxt',
                    'Path to DelfConfig proto text file with configuration to be used for DELG extraction.')
flags.DEFINE_string('query_list_path', '/tmp/query_list.txt',
                    'Text file containing list of query images.')
flags.DEFINE_string('index_list_path', '/tmp/index_list.txt',
                    'Text file containing list of index images.')
flags.DEFINE_string('query_features_dir', '/tmp/features/query',
                    'Directory where query DELG features are located.')
flags.DEFINE_string('index_features_dir', '/tmp/features/index',
                    'Directory where index DELG features are located.')
flags.DEFINE_boolean('use_geometric_verification', False,
                     'If True, performs re-ranking using local feature-based geometric verification.')
flags.DEFINE_float('local_descriptor_matching_threshold', 1.0,
                   'Optional, only used if `use_geometric_verification` is True.')
flags.DEFINE_float('ransac_residual_threshold', 20.0,
                   'Optional, only used if `use_geometric_verification` is True.')
flags.DEFINE_string('output_dir', '/tmp/retrieval',
                    'Directory where retrieval output will be written to.')

FLAGS = flags.FLAGS

def read_image_list(file_path):
    """Reads a text file containing image names and returns it as a list."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main(argv):
    if len(argv) > 1:
        raise RuntimeError('Too many command-line arguments.')

    # Load image lists from text files
    query_list = read_image_list(FLAGS.query_list_path)
    index_list = read_image_list(FLAGS.index_list_path)

    # Read global features
    query_global_features = _ReadDelgGlobalDescriptors(FLAGS.query_features_dir, query_list)
    index_global_features = _ReadDelgGlobalDescriptors(FLAGS.index_features_dir, index_list)

    # Compute similarities and potentially re-rank using geometric verification
    similarities = np.dot(query_global_features, index_global_features.T)
    best_match_indices = np.argmax(similarities, axis=1)

    # Save best match results
    save_best_matches(FLAGS.output_dir, query_list, index_list, best_match_indices)

    # Additional geometric verification could be implemented here if needed

    # Create output directory if necessary
    if not tf.io.gfile.exists(FLAGS.output_dir):
        tf.io.gfile.makedirs(FLAGS.output_dir)

    # Placeholder for further operations, e.g., saving results, calculating metrics, etc.

def _ReadDelgGlobalDescriptors(input_dir, image_list):
    """Reads DELG global features for given list of images."""
    num_images = len(image_list)
    global_descriptors = []
    for i, image_name in enumerate(image_list):
        descriptor_filename = image_name + '.delg_global'
        descriptor_fullpath = os.path.join(input_dir, descriptor_filename)
        global_descriptors.append(datum_io.ReadFromFile(descriptor_fullpath))
    return np.array(global_descriptors)

def save_best_matches(output_dir, query_list, index_list, best_match_indices):
    best_match_filename = os.path.join(output_dir, 'best_matches.txt')
    with open(best_match_filename, 'w') as file:
        for i, query in enumerate(query_list):
            best_match_image = index_list[best_match_indices[i]]
            file.write(f'{query}: {best_match_image}\n')
    print(f'Best matches saved to {best_match_filename}')

if __name__ == '__main__':
    app.run(main)