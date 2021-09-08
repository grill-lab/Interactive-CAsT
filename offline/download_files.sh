#!/bin/bash

echo "Downloading duplicates files"
wget https://raw.githubusercontent.com/daltonj/treccastweb/master/2021/duplicate_files/marco_duplicates.txt -P ./data/duplicates_files
wget https://raw.githubusercontent.com/daltonj/treccastweb/master/2021/duplicate_files/wapo-near-duplicates -P ./data/duplicates_files

echo "Downloading raw collections"
wget --user TRECWaPoSt --ask-password https://ir.nist.gov/wapo/WashingtonPost.v4.tar.gz ./data/collections
wget http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json -P ./data/collections
wget https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docs.tsv.gz -P ./data/collections

echo "Extracting compressed files"
tar -xvf ./data/collections/WashingtonPost.v4.tar.gz WashingtonPost.v4/data/TREC_Washington_Post_collection.v4.jl
mv ./WashingtonPost.v4/data/TREC_Washington_Post_collection.v4.jl ./data/collections
rm -r ./WashingtonPost.v4 ./data/collections/WashingtonPost.v4.tar.gz

gzip -d ./data/collections/msmarco-docs.tsv.gz

echo "Done!"