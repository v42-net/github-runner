#!/bin/bash
set -e
cd $(dirname $0)
GITHUB_ORGANIZATION=v42-net

# (re)create the docker secret from ../secret.txt
SECRET=github-runner.$GITHUB_ORGANIZATION
set +e
docker secret rm $SECRET >/dev/null 2>&1
set -e
docker secret create $SECRET ../secret.txt

# compose the github-runner environment in service.env
rm -rf service.env
for key in HTTP_PROXY HTTPS_PROXY NO_PROXY http_proxy https_proxy no_proxy; do
  if [ -n "${!key}" ] ; then
    echo $key=${!key} >>service.env
  fi
done
echo GITHUB_ORGANIZATION=$GITHUB_ORGANIZATION >>service.env
echo GITHUB_RUNNER_NAME=$(hostname -f) >>service.env
echo GITHUB_RUNNER_GROUP= >>service.env
echo GITHUB_RUNNER_LABELS= >>service.env
echo GITHUB_ACCESS_TOKEN_FILE=/run/secrets/$SECRET >>service.env

# pull the image, create and start the service
IMAGE=ghcr.io/v42-net/github-runner:latest
NAME=github-runner-$GITHUB_ORGANIZATION
FILE=service.env
docker pull $IMAGE
echo $NAME
docker service create --secret $SECRET --name $NAME --env-file $FILE $IMAGE
