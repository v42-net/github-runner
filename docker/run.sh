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
echo GITHUB_ACCESS_TOKEN=$(cat ../secret.txt) >>run.env
echo GITHUB_RUNNER_NAME=$(hostname -f) >>run.env

# pull and run the github-runner image
IMAGE=ghcr.io/v42-net/github-runner:latest
NAME=github-runner.$GITHUB_ORGANIZATION
FILE=./run.env
docker pull $IMAGE
docker run -dit --restart always --name $NAME --env-file $FILE $IMAGE
