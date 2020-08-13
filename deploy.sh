set -e

IMAGE="etweisberg/databank"
GIT_VERSION=$(git describe --always --abbrev --tags --long)

docker build -t ${IMAGE}:${GIT_VERSION} databank
docker tag ${IMAGE}:${GIT_VERSION} ${IMAGE}:latest

echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
docker push ${IMAGE}:${GIT_VERSION}

#ssh commands
ssh -i etweisberg/databank/deploy_key root@159.89.232.85

docker stop current-container
docker rm current-container
docker run --name=current-container --restart unless-stopped -d -p 80:5000 ${IMAGE}:${GIT_VERSION}
docker system prune -a -f
