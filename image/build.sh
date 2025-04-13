#!/bin/bash
set -e

apt-get update -y
apt-get install -y python3-requests

chown runner:runner /home/runner /home/runner/control.py
chmod 0755 /home/runner/control.py

apt-get -y clean
rm -rf /var/lib/apt/lists/*
rm -rf /build*
