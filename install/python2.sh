#!/bin/bash
set -Eeuxo pipefail

apt-get install -y --no-install-recommends python2 python-pip
python2 -m pip install virtualenv

