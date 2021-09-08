# Builder

This service compiles the protocol buffers and grpc services that the online system uses.

# How to run

1. Build the docker image:

`docker build -t cast-searcher-builder-image .`

2. Run and exec into the docker image, mounting the current directory and `shared` directory as volumes:

`docker run -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-builder-image`