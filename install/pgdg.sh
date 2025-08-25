#!/bin/bash
set -Eeuxo pipefail

true \
 && apt update -yq \
 && apt install -yq --no-install-recommends \
      gnupg ca-certificates postgresql-common \
 && rm -rf /var/lib/apt/lists/*

/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y
