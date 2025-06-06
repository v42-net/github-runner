#!/bin/bash
set -e
cd $(dirname $0)
GITHUB_ORGANIZATION=v42-net

# compose the github-runner environment in run.env
rm -rf run.env
for key in HTTP_PROXY HTTPS_PROXY NO_PROXY http_proxy https_proxy no_proxy; do
  if [ -n "${!key}" ] ; then
    echo $key=${!key} >>run.env
  fi
done
echo GITHUB_ORGANIZATION=$GITHUB_ORGANIZATION >>run.env
echo GITHUB_RUNNER_NAME=$(hostname -f) >>run.env
echo GITHUB_RUNNER_GROUP= >>run.env
echo GITHUB_RUNNER_LABELS= >>run.env
echo GITHUB_ACCESS_TOKEN=$(cat ../secret.txt) >>run.env

# pull and start the github-runner image
IMAGE=ghcr.io/v42-net/github-runner:latest
NAME=github-runner-$GITHUB_ORGANIZATION
FILE=./run.env
docker pull $IMAGE
docker run -it --rm --name $NAME --env-file $FILE $IMAGE
