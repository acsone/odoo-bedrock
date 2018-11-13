#!/bin/bash
set -Eeuxo pipefail

if [ "${PYTHONBIN}" != "python3.6" ] ; then
    # ubuntu 18 has pyton 3.6 only, so use the deadsnakes ppa
    apt-get install -y --no-install-recommends software-properties-common
    add-apt-repository -y ppa:deadsnakes/ppa
    apt-get install -y --no-install-recommends ${PYTHONBIN}-venv
    apt-get purge -y --auto-remove software-properties-common
else
    # ubuntu 18 has pyton 3.6
    apt-get install -y --no-install-recommends ${PYTHONBIN}-venv
fi
