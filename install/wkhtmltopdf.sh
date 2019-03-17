#!/bin/bash
set -eo pipefail
curl -o /usr/local/bin/wkhtmltopdf -SL https://github.com/acsone/kwkhtmltopdf/releases/download/0.9.0/kwkhtmltopdf_client
echo "49b609de7e7964b65c2021e71f651eb1c5f76112 /usr/local/bin/wkhtmltopdf" | sha1sum -c -
chmod +x /usr/local/bin/wkhtmltopdf
