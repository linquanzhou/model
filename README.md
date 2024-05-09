##0 setup

cd research
export PYTHONPATH=$PYTHONPATH:`pwd`
cd delf
~/models/tf-slim/bin/protoc delf/protos/*.proto --python_out=.
pip3 install -e .
python3 -c 'import delf'


##1 train model

python3 build_image_dataset.py \
  --train_csv_path=gldv2_dataset/train/train.csv \
  --train_clean_csv_path=gldv2_dataset/train/train_clean.csv \
  --train_directory=gldv2_dataset/train/\*/\*/\*/ \
  --output_directory=gldv2_dataset/tfrecord/ \
  --num_shards=128 \
  --generate_train_validation_splits \
  --validation_split_size=0.2

  python3 train.py \
  --train_file_pattern='gldv2_dataset/tfrecord/train*' \
  --validation_file_pattern='gldv2_dataset/tfrecord/validation*' \
  --imagenet_checkpoint='resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5' \
  --dataset_version='gld_v2_clean' \
  --logdir='gldv2_training/' \
  --delg_global_features \
  --debug

##2 extract features

python3 extract_features.py \
  --delf_config_path my_model_config.pbtxt \
  --query_list_path ~/delg/delg_test/query_list.txt \
  --images_dir ~/delg/delg_test/data/query_image \
  --image_set query \
  --output_features_dir ~/delg/delg_test/data/feature/query_feature

python3 extract_features.py \
  --delf_config_path my_model_config.pbtxt \
  --index_list_path ~/delg/delg_test/gld_index_list.txt \
  --images_dir ~/delg/delg_test/data\gld_index \
  --image_set index \
  --output_features_dir ~/delg/delg_test/data/gld_features/index_test


##3 compare

python3 perform_retrieval.py \
  --query_list_path ~/delg/delg_test/query_list.txt \
  --index_list_path ~/delg/delg_test/gld_index_list.txt \
  --query_features_dir ~/delg/delg_test/data/feature/query_feature \
  --index_features_dir ~/delg/delg_test/data/gld_index \
  --output_dir ~/delg/delg_test/results/test

##4 visualization

python visualization.py --data_directory ~/delg/delg_test/data/gld_index --matches_file ~/delg/delg_test/results/test/best_matches.txt --output_file 'unique_labels.txt' --max_rows 100

##5 generate map

python map.py
