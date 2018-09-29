#!/bin/bash
set -Eeuo pipefail

# allow to customize the UID of the odoo user,
# so we can share the same than the host's.
# If no user id is set, we use 999
USER_ID=${LOCAL_USER_ID:-999}

echo "Starting with UID : $USER_ID"
id -u odoo &> /dev/null || useradd --shell /bin/bash -u $USER_ID -o -c "" -m odoo

confd -log-level=warn -onetime -backend ${CONFD_BACKEND:-env} ${CONFD_OPTS:-}

# TODO this could (should?) be sourced from file(s) under confd control
export PGHOST=${DB_HOST}
export PGPORT=${DB_PORT}
export PGUSER=${DB_USER}
export PGPASSWORD=${DB_PASSWORD}
export PGDATABASE=${DB_NAME}

mkdir -p /data/odoo/{addons,filestore,sessions}
if [ ! "$(stat -c '%U' /data/odoo)" = "odoo" ]; then
  chown -R odoo: /data/odoo
fi

if [ -z "${NOGOSU:-}" ] ; then

  START_ENTRYPOINT_DIR=/odoo/start-entrypoint.d
  if [ -d "$START_ENTRYPOINT_DIR" ]; then
    run-parts --verbose "$START_ENTRYPOINT_DIR"
  fi

  exec gosu odoo "$@"
else
  exec "$@"
fi
