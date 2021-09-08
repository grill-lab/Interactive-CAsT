# Offline Index Preparation Pipeline

The `offline` pipeline prepares and processes the raw collection into a lucene index that is used within the online system. The three main steps of the pipeline are:

## Passage Chunking

Todo

Add description


## Trecweb Conversion

Todo

Add description

## Index Generation

Todo

Add description


# How to run

1. Download the raw collations (This might take a while!):

`bash download_files.sh`

2. Build the docker image:

`docker build -t cast-searcher-offline-image .`

3. Run and exec into the docker image, mounting the current directory and `shared` directory as volumes:

`docker run -it -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-offline-image bash`

4. Run `python3 main.py`, 