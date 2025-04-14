#!/bin/bash
set -e
cd $(dirname $0)
source ../.project
TAGS="-t $IMAGE:$BRANCH"
if [ "$BRANCH" = "main" ]; then
  TAGS="$TAGS -t $IMAGE:latest"
fi
docker pull ghcr.io/actions/actions-runner:latest
docker build --no-cache --progress=plain $TAGS ..
echo docker login ghcr.io
docker login ghcr.io
docker push -a $IMAGE
