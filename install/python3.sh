#!/bin/bash
set -Eeuxo pipefail

source /etc/os-release
if [ "${UBUNTU_CODENAME}" == "bionic" ] ; then
    SYSTEM_PYTHON=python3.6
elif [ "${UBUNTU_CODENAME}" == "focal" ] ; then
    SYSTEM_PYTHON=python3.8
elif [ "${UBUNTU_CODENAME}" == "jammy" ] ; then
    SYSTEM_PYTHON=python3.10
else
    echo "Unknown UBUNTU_CODENAME '${UBUNTU_CODENAME}'"
    exit 1
fi

if [ "${PYTHONBIN}" != "${SYSTEM_PYTHON}" ] ; then
    # use the deadsnakes ppa
    apt-get install -y --no-install-recommends software-properties-common
    add-apt-repository -y ppa:deadsnakes/ppa
    apt-get install -y --no-install-recommends ${PYTHONBIN}-venv
    apt-get purge -y --auto-remove software-properties-common
else
    # use system python
    apt-get install -y --no-install-recommends ${PYTHONBIN}-venv python3-venv
fi
