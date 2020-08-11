set -e

IMAGE="etweisberg/databank"
GIT_VERSION=$(git describe --always --abbrev --tags --long)

docker build -t ${IMAGE}:${GIT_VERSION} databank
docker tag ${IMAGE}:${GIT_VERSION} ${IMAGE}:latest

echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
docker push ${IMAGE}:${GIT_VERSION}

#ssh commands
touch temp_key
echo ${SSH_KEY} > temp_key
chmod 600 temp_key
echo ${PUBLIC_KEY} > pub
chmod 644 pub
ssh-keygen -p -P ${PASS} -N "" -f temp_key
ssh -i temp_key root@159.89.232.85

docker stop current-container
docker rm current-container
docker run --name=current-container --restart unless-stopped -d -p 80:5000 ${IMAGE}:${GIT_VERSION}
docker system prune -a -f
