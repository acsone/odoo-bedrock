#!/bin/bash
set -Eeuxo pipefail

apt-get install -y --no-install-recommends \
  node-clean-css \
  xfonts-75dpi \
  xfonts-base
