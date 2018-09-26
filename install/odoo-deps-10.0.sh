#!/bin/bash
set -Eeuxo pipefail

apt-get install -y --no-install-recommends \
  antiword \
  ghostscript \
  graphviz \
  node-clean-css \
  node-less \
  poppler-utils \
  xfonts-75dpi \
  xfonts-base
