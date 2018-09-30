#!/bin/bash
set -Eeuxo pipefail

apt-get install -y --no-install-recommends \
  node-clean-css \
  node-less \
  xfonts-75dpi \
  xfonts-base
