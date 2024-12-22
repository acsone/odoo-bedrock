#!/bin/bash
set -eo pipefail
curl -o /usr/local/bin/wkhtmltopdf -SL https://github.com/acsone/kwkhtmltopdf/releases/download/1.0/kwkhtmltopdf_client
echo "4856c49a1a20a949548a2535ac98de64873bd167 /usr/local/bin/wkhtmltopdf" | sha1sum -c -
chmod +x /usr/local/bin/wkhtmltopdf
