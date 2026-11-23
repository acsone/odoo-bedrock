#!/bin/bash
#!/bin/bash
set -eo pipefail

source /etc/os-release
if [ "${ODOO_VERSION%%.*}" -lt 20 ]; then
  echo "Paper Muncher is not needed for Odoo $ODOO_VERSION, skipping"
  exit 0
fi

PAPER_MUNCHER_VERSION=0.10.0
# v0.10.0 resolute
PAPER_MUNCHER_SHA256=1c2c642262494d1a31f64811000d04f0c143838fdf823fb96a3c8c968ce58fbf

DEB="paper-muncher_v${PAPER_MUNCHER_VERSION}_${UBUNTU_CODENAME}_amd64.deb"

cd /tmp
curl -o "$DEB" -fSL "https://github.com/odoo/paper-muncher/releases/download/v${PAPER_MUNCHER_VERSION}/${DEB}"
echo "${PAPER_MUNCHER_SHA256} ${DEB}" | sha256sum -c -
apt-get install -y --no-install-recommends "./$DEB"
rm -f "$DEB"

# The package installs into /opt/paper-muncher, which is not in PATH
ln -s /opt/paper-muncher/bin/paper-muncher /usr/local/bin/paper-muncher
