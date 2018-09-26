#!/bin/bash
set -Eeuxo pipefail

apt install -y --no-install-recommends \
  ca-certificates \
  curl \
  less \
  nano
