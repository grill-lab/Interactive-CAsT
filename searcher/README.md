# How to run

1. Build the docker image:

`docker build -t cast-searcher-searcher-image .`

2. Run and exec into the docker image, mounting the current directory and `shared` directory as volumes:

`docker run -it -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-searcher-image bash`

3. For testing

`docker run -p 127.0.0.1:8000:8000 -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-searcher-image`