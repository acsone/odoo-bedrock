#!/bin/bash
set -eo pipefail

apt-get install -y --no-install-recommends xz-utils
curl -o wkhtmltox.tar.xz -SL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
echo '3f923f425d345940089e44c1466f6408b9619562 wkhtmltox.tar.xz' | sha1sum -c -
tar xvf wkhtmltox.tar.xz
cp --no-dereference --preserve=link wkhtmltox/lib/* /usr/local/lib/
cp wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
rm -rf wkhtmltox wkhtmltox.tar.xz
apt-get purge -y --auto-remove xz-utils

apt-get install -y --no-install-recommends \
  ca-certificates \
  fontconfig \
  libc6 \
  libfreetype6 \
  libjpeg-turbo8 \
  libpng16-16 \
  libssl1.1 \
  libstdc++6 \
  libx11-6 \
  libxcb1 \
  libxext6 \
  libxrender1 \
  xfonts-75dpi \
  xfonts-base \
  zlib1g
