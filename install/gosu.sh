#!/bin/bash
set -Eeuxo pipefail

pushd /usr/local/bin

arch=`uname -m`

if [[ $arch = "aarch64" ]]; then
  arch="arm64"
  hash="23fa49907d5246d2e257de3bf883f57fba47fe1f559f7e732ff16c0f23d2b6a6"
else
  arch="amd64"
  hash="3a4e1fc7430f9e7dd7b0cbbe0bfde26bf4a250702e84cf48a1eb2b631c64cf13"
fi
curl -o gosu -SL "https://github.com/tianon/gosu/releases/download/1.16/gosu-${arch}"
echo "${hash} gosu" | sha256sum -c -
chmod +x gosu
popd

# verify that the binary works
gosu nobody true
