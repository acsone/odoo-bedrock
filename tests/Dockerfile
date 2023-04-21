# Dockerfile to run tests
ARG IMAGE=ghcr.io/acsone/odoo-bedrock
ARG ODOOVERSION=16.0
ARG PYTHONTAG=py310

FROM $IMAGE:$ODOOVERSION-$PYTHONTAG-latest

# Fake odoo command in PATH
RUN echo "#!/bin/bash\necho running odoo UID=\$(id -u)\n" > /odoo/bin/odoo \
 && chmod +x /odoo/bin/odoo

# Fake entry points
RUN mkdir -p /odoo/start-entrypoint.d \
 && echo "#!/bin/bash\necho entrypoint 1 UID=\$(id -u)\n" > /odoo/start-entrypoint.d/01-test \
 && echo "#!/bin/bash\necho entrypoint 2 UID=\$(id -u)\n" > /odoo/start-entrypoint.d/02-test \
 && chmod +x /odoo/start-entrypoint.d/0*-test
