# Odoo Bedrock container image

This image is meant as a greatest common denominator foundation to run
Odoo.

It is a BYOO (bring-your-own-odoo) image, which means you need to create
a derived image that adds your Odoo and addons. This image does not
mandate any particular installation method for Odoo and addons, nor does
it impose any constraint on your project structure.

## Available image tags

The CI of this project builds regularly for some combinations of Odoo
version, python version and Ubuntu version.

The supported combinations are visible in the [build
matrix](./.github/workflows/ci.yml).

## Features exposed by these images

> [!NOTE]
> Anything not documented here considered implementation detail and may
> change.

- Ubuntu minimal because it's small and has recent pythons
- `python`, obviously, in an activated virtual environment.
- An entrypoint that generates the Odoo config file (`$ODOO_RC`) from
  environment variables (see the list of supported variables below).
- `/usr/local/bin/wkhtmltopdf` is the
  [kwkhtmltopdf](https://github.com/acsone/kwkhtmltopdf) client. The
  default KWKHTMLTOPDF_SERVER_URL environment variable is set to
  <http://kwkhtmltopdf>.
- Odoo mandatory external dependencies (i.e. `lessc` for Odoo \< 12)
- `nano`, `less`, for some rudimentary comfort when the time comes to
  investigate the container on the terminal
- postgres [apt repo](https://wiki.postgresql.org/wiki/Apt) for easy
  installation of the latest postgres client tools if needed

Note **Odoo's python dependencies are not included**: you need to pip
install Odoo's `requirements.txt`, or apt install them. This is not done
in the base image as different projects may require different versions
of these libraries.

Other dependencies are also notably absent (graphviz, antiword,
poppler-utils), these being unused in the latest Odoo version and
infrequently used in older versions.

The entrypoint does the following:

- Generate the `$ODOO_RC` file from environment variables
- If the command looks like odoo, run scripts in
  `/odoo/start-entrypoint.d/`.
- Unless `$NOGOSU` is set, run the entry point scripts, as well as the
  command, under user `$LOCAL_USER_ID` (defaults to 999).

For more details, read [./bin/entrypoint.sh](./bin/entrypoint.sh).

### Configuration

The following environment variables are used to generate the Odoo
configuration file in `$ODOO_RC`.

Odoo options:

- `ADDONS_PATH`
- `ADMIN_PASSWD`
- `DB_FILTER`
- `DB_HOST`
- `DB_REPLICA_HOST` (\>=18)
- `DB_MAXCONN`
- `DB_MAXCONN_GEVENT` (\>=17)
- `DB_NAME`
- `DB_PASSWORD`
- `DB_PORT`
- `DB_REPLICA_PORT` (\>=18)
- `DB_SSLMODE`
- `DB_TEMPLATE`
- `DB_USER`
- `LIMIT_MEMORY_HARD`
- `LIMIT_MEMORY_HARD_GEVENT` (\>=18)
- `LIMIT_MEMORY_SOFT`
- `LIMIT_MEMORY_SOFT_GEVENT` (\>=18)
- `LIMIT_REQUEST`
- `LIMIT_TIME_CPU`
- `LIMIT_TIME_REAL`
- `LIMIT_TIME_REAL_CRON` (\>=11)
- `LIST_DB`
- `LOG_DB`
- `LOG_HANDLER`
- `LOG_LEVEL`
- `LOGFILE`
- `MAX_CRON_THREADS`
- `SERVER_WIDE_MODULES` (\>=10)
- `SYSLOG`
- `UNACCENT`
- `WITHOUT_DEMO`
- `WORKERS`

Other variables that populate `$ODOO_RC`:

- `RUNNING_ENV`: sets `options.running_env` for use by the [OCA
  server_environment](https://github.com/OCA/server-env) module.
- `ADDITIONAL_ODOO_RC`: is appended verbatim a the end of `$ODOO_RC`.

The following environment variables are processed by the entrypoint, if
the `psql` client is installed (which is not the case by default):

- `ODOO_BASE_URL` sets the `web.base.url` system parameter, and forces
  `web.base.urL.freeze` to `True`.
- `ODOO_REPORT_URL` sets the `report.url` system parameter.

## Example

This is a typical Dockerfile derived from this image, provided here for
inspiration.

Assume you have your custom addons in `myaddons`. You can create the
following Dockerfile:

```dockerfile
ARG odoo_version=17.0

###########################################################################
# build stage, install Odoo

FROM ghcr.io/acsone/odoo-bedrock:${odoo_version}-py312-jammy-latest AS build

ARG odoo_version

# Install build dependencies
RUN apt -yq update \
&& apt -yq install --no-install-recommends \
   curl \
   python3.12-dev \
   build-essential \
   libpq-dev \
   libldap2-dev \
   libsasl2-dev \
&& rm -rf /var/lib/apt/lists/*

ADD https://raw.githubusercontent.com/odoo/odoo/${odoo_version}/requirements.txt /odoo/src/odoo/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /odoo/src/odoo/requirements.txt

ADD https://api.github.com/repos/odoo/odoo/git/refs/heads/${odoo_version} /tmp/odoo_version.json
RUN curl -sSL https://github.com/odoo/odoo/tarball/${odoo_version} | tar -C /odoo/src/odoo --strip-components=1 -xz
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -e /odoo/src/odoo --config-setting editable_mode=compat

###########################################################################
# runtime stage

FROM ghcr.io/acsone/odoo-bedrock:${odoo_version}-py312-jammy-latest

# Install runtime system dependencies
RUN apt -yq update \
&& apt -yq install --no-install-recommends \
   postgresql-client \
&& rm -rf /var/lib/apt/lists/*

# Copy venv from build stage to runtime stage
COPY --from=build /odoo /odoo

COPY ./myaddons /odoo/src/myaddons

ENV ADDONS_PATH=/odoo/src/odoo/addons,/odoo/src/odoo/odoo/addons,/odoo/src/myaddons
```

## Credits

Inspiration has been drawn from
[camptocamp/docker-odoo-project](https://github.com/camptocamp/docker-odoo-project)
for most environment variables, the odoo config file templates, and
entrypoint.sh. This is by design, in order to facilitate possible future
convergence.

[Contributors](https://github.com/acsone/odoo-bedrock/graphs/contributors).
