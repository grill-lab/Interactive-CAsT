cd ..
echo Going to base of repo at $PWD

echo Setting docker environemt to host
minikube docker-env --unset

echo Building bob the builder
sudo docker build -t cast-searcher-builder-image -f builder/Dockerfile .
docker run -v $PWD/../shared:/shared -v $PWD:/source cast-searcher-builder-image

echo Setting docker environemt to minikube
eval $(minikube docker-env)

echo Building reranker image
docker build -t cast-searcher-reranker-image -f reranker/Dockerfile .

echo Building rewriter image
docker build -t cast-searcher-rewriter-image -f rewriter/Dockerfile .

echo Builing searcher image
docker build -t cast-searcher-searcher-image -f searcher/Dockerfile .

echo Builing web_ui image
docker build -t cast-searcher-web-ui-image -f web_ui/Dockerfile .