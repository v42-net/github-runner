#!/bin/bash
set -e
cd $(dirname $0)
FULLHOSTNAME=$(hostname -f) docker compose up -d
