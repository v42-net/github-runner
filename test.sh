#!/bin/bash
set -e
cd $(dirname $0)
REPO=$(git config --get remote.origin.url)
REPO="${REPO,,}"
REPO="${REPO%.*}"
NAME=$(basename $REPO)
OWNER=$(basename $(dirname $REPO))
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REGISTRY=ghcr.io
IMAGE=$REGISTRY/$OWNER/$NAME:$BRANCH
HOSTNAME=$(hostname -f)

clear
#./build.sh
echo ""
docker run --rm -it --name $NAME --hostname $HOSTNAME --env-file config.env ghcr.io/v42-net/github-runner:latest
echo ""
