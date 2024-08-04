# Test suite

This test suite relies on a test harness composed of a [Dockerfile](./Dockerfile) based
on the `odoo-bedrock` images, as well as a [docker-compose.yml](./docker-compose.yml).

Prerequisites to run the test suite are `python3`, `docker compose` and `pytest`
installed in the python environment.

Tests are launched with `pytest -v ./tests`. They start with a `docker compose build`
using the `PYTHONTAG`, `DISTRO` and `ODOOVERSION` environment variables to determine the
base `odoo-bedrock` image.
