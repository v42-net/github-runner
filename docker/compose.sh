#!/bin/bash
set -e
cd $(dirname $0)
GITHUB_ORGANIZATION=v42-net

# compose the github-runner environment in compose.env
rm -rf service.env
for key in HTTP_PROXY HTTPS_PROXY NO_PROXY http_proxy https_proxy no_proxy; do
  if [ -n "${!key}" ] ; then
    echo $key=${!key} >>compose.env
  fi
done

echo GITHUB_ORGANIZATION=$GITHUB_ORGANIZATION >>compose.env
echo GITHUB_RUNNER_NAME=$(hostname -f) >>compose.env
echo GITHUB_RUNNER_GROUP= >>compose.env
echo GITHUB_RUNNER_LABELS= >>compose.env
echo GITHUB_ACCESS_TOKEN_FILE=/run/secrets/GITHUB_ACCESS_TOKEN >>compose.env

# pull the image start the service
docker compose pull
docker compose up -d
