# Dockerfile to run tests

# /!\ These defaults must match those in conftest.py
ARG IMAGE=ghcr.io/acsone/odoo-bedrock
ARG ODOOVERSION=16.0
ARG PYTHONTAG=py310
ARG DISTRO=jammy

FROM $IMAGE:$ODOOVERSION-$PYTHONTAG-$DISTRO-latest

RUN apt-get update && apt-get install -y postgresql-client --no-install-recommends

# Fake odoo command in PATH
RUN echo "#!/bin/bash\necho running odoo UID=\$(id -u)\n" > /odoo/bin/odoo \
 && chmod +x /odoo/bin/odoo \
 && cp /odoo/bin/odoo /odoo/bin/openerp-server

# Fake entry points
RUN mkdir -p /odoo/start-entrypoint.d \
 && echo "#!/bin/bash\necho entrypoint 1 UID=\$(id -u)\n" > /odoo/start-entrypoint.d/01-test \
 && echo "#!/bin/bash\necho entrypoint 2 UID=\$(id -u)\n" > /odoo/start-entrypoint.d/02-test \
 && chmod +x /odoo/start-entrypoint.d/0*-test
