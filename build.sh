#!/bin/bash
set -e
cd $(dirname $0)
REPO=$(git config --get remote.origin.url)
REPO="${REPO,,}"
REPO="${REPO%.*}"
NAME=$(basename $REPO)
OWNER=$(basename $(dirname $REPO))
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Determine the image tags
# ------------------------
REGISTRY=ghcr.io
IMAGE=$REGISTRY/$OWNER/$NAME
TAGS="-t $IMAGE:$BRANCH"
if [ "$BRANCH" = "main" ]; then
  TAGS="$TAGS -t $IMAGE:latest"
fi

# pull, build and push the docker image
# -------------------------------------
docker pull ghcr.io/actions/actions-runner:latest
docker build --no-cache --progress=plain $TAGS $ARGS .
echo docker login $REGISTRY
docker login $REGISTRY
docker push -a $IMAGE
