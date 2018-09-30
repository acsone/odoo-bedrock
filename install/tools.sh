#!/bin/bash
set -Eeuxo pipefail

apt-get install -y --no-install-recommends \
  ca-certificates \
  less \
  nano
