from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from absl import app
from absl import flags
import numpy as np
import tensorflow as tf

from google.protobuf import text_format
from delf import delf_config_pb2
from delf import datum_io
from delf import feature_io
from delf import utils
from delf.python.datasets.revisited_op import dataset
from delf import extractor

import os
import time
import numpy as np
import tensorflow as tf
from absl import app, flags
from PIL import Image
from delf import delf_config_pb2
from delf import datum_io
from delf import feature_io
from delf import extractor
from delf import utils

flags.DEFINE_string(
    'delf_config_path', '/tmp/delf_config_example.pbtxt',
    'Path to DelfConfig proto text file with configuration to be used for DELG '
    'extraction.')
flags.DEFINE_string(
    'query_list_path', '/tmp/query_list.txt',
    'Text file containing list of query images.')
flags.DEFINE_string(
    'index_list_path', '/tmp/index_list.txt',
    'Text file containing list of index images.')
flags.DEFINE_string(
    'images_dir', '/tmp/images',
    'Directory where dataset images are located, all in .jpg format.')
flags.DEFINE_enum('image_set', 'query', ['query', 'index'],
                  'Whether to extract features from query or index images.')
flags.DEFINE_string(
    'output_features_dir', '/tmp/features',
    "Directory where DELG features will be written to.")

FLAGS = flags.FLAGS
_STATUS_CHECK_ITERATIONS = 50


def read_image_list(file_path):
    """Reads a text file containing image names and returns it as a list."""
    with open(file_path, 'r') as file:
        image_list = [line.strip() for line in file.readlines()]
    return image_list

def main(argv):
    if len(argv) > 1:
        raise RuntimeError('Too many command-line arguments.')

    # Load image lists from text files
    if FLAGS.image_set == 'query':
        image_list = read_image_list(FLAGS.query_list_path)
    else:
        image_list = read_image_list(FLAGS.index_list_path)
    num_images = len(image_list)
    print(f'Found {num_images} images')

    # Parse DelfConfig proto.
    config = delf_config_pb2.DelfConfig()
    with tf.io.gfile.GFile(FLAGS.delf_config_path, 'r') as f:
        text_format.Parse(f.read(), config)

    # Create output directory if necessary.
    if not tf.io.gfile.exists(FLAGS.output_features_dir):
        tf.io.gfile.makedirs(FLAGS.output_features_dir)

    extractor_fn = extractor.MakeExtractor(config)
    start = time.time()
    for i, image_name in enumerate(image_list):
        input_image_filename = os.path.join(FLAGS.images_dir, image_name + '.jpg')

        # Compose output file names
        output_global_feature_filename = os.path.join(
            FLAGS.output_features_dir, image_name + '.delg_global')
        output_local_feature_filename = os.path.join(
            FLAGS.output_features_dir, image_name + '.delg_local')

        # Check if features need to be extracted
        should_skip_global = tf.io.gfile.exists(output_global_feature_filename)
        should_skip_local = tf.io.gfile.exists(output_local_feature_filename)
        if should_skip_global and should_skip_local:
            print('Skipping', image_name)
            continue

        pil_im = utils.RgbLoader(input_image_filename)
        im = np.array(pil_im)

        # Extract and save features.
        extracted_features = extractor_fn(im, 1.0)  # Assume no resize needed
        if config.use_global_features and not should_skip_global:
            global_descriptor = extracted_features['global_descriptor']
            datum_io.WriteToFile(global_descriptor, output_global_feature_filename)
        if config.use_local_features and not should_skip_local:
            locations = extracted_features['local_features']['locations']
            descriptors = extracted_features['local_features']['descriptors']
            feature_scales = extracted_features['local_features']['scales']
            attention = extracted_features['local_features']['attention']
            feature_io.WriteToFile(output_local_feature_filename, locations, feature_scales, descriptors, attention)

        if (i + 1) % _STATUS_CHECK_ITERATIONS == 0:
            elapsed = (time.time() - start)
            print(f'Processing image {i + 1} out of {num_images}, last {_STATUS_CHECK_ITERATIONS} images took {elapsed:.2f} seconds')
            start = time.time()

if __name__ == '__main__':
    app.run(main)