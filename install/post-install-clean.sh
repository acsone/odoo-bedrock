#!/bin/bash
set -Eeuxo pipefail

apt-get purge -y --auto-remove curl
apt-get clean
rm -rf /var/lib/apt/lists/* /root/.cache/pip/*
