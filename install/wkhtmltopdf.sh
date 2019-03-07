#!/bin/bash
set -eo pipefail
curl -o /usr/local/bin/wkhtmltopdf -SL https://raw.githubusercontent.com/acsone/kwkhtmltopdf/master/client/python/kwkhtmltopdf_client.py
chmod +x /usr/local/bin/wkhtmltopdf
