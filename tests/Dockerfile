# Dockerfile to run tests
ARG IMAGE=ghcr.io/acsone/odoo-bedrock
ARG ODOOVERSION=16.0
ARG PYTHONTAG=py310

FROM $IMAGE:$ODOOVERSION-$PYTHONTAG-latest AS with-psql

RUN pip install pytest
RUN echo "#!/bin/bash\necho running odoo UID=\$(id -u)\n" > /odoo/bin/odoo \
 && chmod +x /odoo/bin/odoo

RUN echo "#!/bin/bash\necho entrypoint 1 UID=\$(id -u)\n" > /odoo/start-entrypoint.d/01-test \
 && echo "#!/bin/bash\necho entrypoint 2 UID=\$(id -u)\n" > /odoo/start-entrypoint.d/02-test \
 && chmod +x /odoo/start-entrypoint.d/0*-test
