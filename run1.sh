#!/bin/sh
set -e

apt-get update
apt-get install -y --no-install-recommends build-essential
rm -rf /var/lib/apt/lists/*
