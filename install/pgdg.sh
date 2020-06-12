#!/bin/bash
set -Eeuxo pipefail

source /etc/os-release
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt ${UBUNTU_CODENAME}-pgdg main" > /etc/apt/sources.list.d/pgdg.list
