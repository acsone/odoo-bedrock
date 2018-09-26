#!/bin/bash
set -eo pipefail

pushd /usr/local/bin
curl -SL -o confd https://github.com/kelseyhightower/confd/releases/download/v0.16.0/confd-0.16.0-linux-amd64
echo '255d2559f3824dd64df059bdc533fd6b697c070db603c76aaf8d1d5e6b0cc334  confd' | sha256sum -c -
chmod +x confd
popd
