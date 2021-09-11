# Testing

To run the service in isolation for testing purposes, you may try the following:

1. Build the docker image:

`docker build -t cast-searcher-rewriter-image .`

2. Run and exec into the docker container, mounting the current directory and `shared` directory as volumes:

`docker run -it -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-rewriter-image bash`

or

3.  Run the container as an endpoint on your host machine to make calls to (the code in the main.py of the `web_ui` service is an example of how to make such calls.)

`docker run -p 127.0.0.1:6000:8000 -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-rewriter-image`