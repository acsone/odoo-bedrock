from pathlib import Path
import os
import subprocess
import time

import pytest

from .testlib import compose_run

HERE = Path(__file__).parent


@pytest.fixture(scope="session", autouse=True)
def compose_build():
    cmd = ["docker-compose", "build"]
    if "ODOOVERSION" in os.environ:
        cmd.extend(["--build-arg", f"ODOOVERSION={os.environ['ODOOVERSION']}"])
    if "PYTHONTAG" in os.environ:
        cmd.extend(["--build-arg", f"PYTHONTAG={os.environ['PYTHONTAG']}"])
    subprocess.run(cmd, check=True, cwd=HERE)


@pytest.fixture(scope="session")
def odoo_version():
    # /!\ Default must be the same as the ODOOVERSION build arg in test Dockerfile
    return os.environ.get("ODOOVERSION", "16.0")


@pytest.fixture(scope="session")
def parsed_odoo_version(odoo_version):
    return tuple(int(x) for x in odoo_version.split("."))


@pytest.fixture(scope="session")
def compose_up(compose_build):
    subprocess.run(["docker-compose", "up", "-d"], check=True, cwd=HERE)
    try:
        while compose_run(["pg_isready"], check=False).returncode != 0:
            time.sleep(2)
        yield
    finally:
        subprocess.run(["docker-compose", "down"], check=True, cwd=HERE)


@pytest.fixture
def init_odoo_db(compose_up):
    """Fake Odoo database initialization."""
    CREATE_IR_CONFIG_PARAMETERS = """
        CREATE TABLE ir_config_parameter
        (
            create_uid integer,
            write_uid integer,
            create_date timestamp without time zone,
            write_date timestamp without time zone,
            key character varying NULL,
            value text NOT NULL
        )
    """
    DROP_IR_CONFIG_PARAMETERS = "DROP TABLE ir_config_parameter"
    compose_run(["psql", "-c", CREATE_IR_CONFIG_PARAMETERS])
    try:
        yield
    finally:
        compose_run(["psql", "-c", DROP_IR_CONFIG_PARAMETERS])
