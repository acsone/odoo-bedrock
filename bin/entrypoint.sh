#!/bin/bash
set -Eeuo pipefail

# allow to customize the UID of the odoo user,
# so we can share the same than the host's.
# If no user id is set, we use 999
USER_ID=${LOCAL_USER_ID:-999}

id -u odoo &> /dev/null || useradd --shell /bin/bash -u $USER_ID -o -c "" -m odoo

source /odoo/templates/answers.sh && envsubst < /odoo/templates/odoo.cfg.tmpl > /etc/odoo.cfg

mkdir -p /data/odoo/{addons,filestore,sessions}
if [ ! "$(stat -c '%U' /data/odoo)" = "odoo" ]; then
  chown -R odoo: /data/odoo
fi

if [ -z "${NOGOSU:-}" ] ; then
  echo "Starting with UID: $USER_ID"
fi

BASE_CMD=$(basename $1)
if [ "$BASE_CMD" = "odoo" ] || [ "$BASE_CMD" = "odoo.py" ] || [ "$BASE_CMD" = "odoo-bin" ] || [ "$BASE_CMD" = "openerp-server" ] ; then
  START_ENTRYPOINT_DIR=/odoo/start-entrypoint.d
  if [ -d "$START_ENTRYPOINT_DIR" ]; then
    if [ -z "${NOGOSU:-}" ] ; then
      gosu odoo run-parts --exit-on-error --verbose "$START_ENTRYPOINT_DIR"
    else
      run-parts --exit-on-error --verbose "$START_ENTRYPOINT_DIR"
    fi
  fi
fi

if [ -z "${NOGOSU:-}" ] ; then
  exec gosu odoo "$@"
else
  exec "$@"
fi
