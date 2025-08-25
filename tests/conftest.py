from pathlib import Path
import os
import subprocess
import time

import pytest

from .testlib import compose_run

HERE = Path(__file__).parent

# /!\ These defaults must match those in Dockerfile
DEFAULT_TEST_IMAGE = "ghcr.io/acsone/odoo-bedrock"
DEFAULT_TEST_ODOOVERSION = "16.0"
DEFAULT_TEST_PYTHONTAG = "py310"
DEFAULT_TEST_DISTRO = "jammy"


@pytest.fixture(scope="session")
def odoo_version():
    return os.environ.get("ODOOVERSION", DEFAULT_TEST_ODOOVERSION)


@pytest.fixture(scope="session")
def python_tag():
    return os.environ.get("PYTHONTAG", DEFAULT_TEST_PYTHONTAG)


@pytest.fixture(scope="session")
def python_bin(python_tag):
    return f"python{python_tag[2:3]}.{python_tag[3:]}"


@pytest.fixture(scope="session")
def distro():
    return os.environ.get("DISTRO", DEFAULT_TEST_DISTRO)


@pytest.fixture(scope="session", autouse=True)
def compose_build(odoo_version, python_tag, python_bin, distro):
    docker_build_options = [
        "--build-arg",
        f"ODOOVERSION={odoo_version}",
        "--build-arg",
        f"PYTHONTAG={python_tag}",
        "--build-arg",
        f"PYTHONBIN={python_bin}",
        "--build-arg",
        f"DISTRO={distro}",
    ]
    if "BUILDER" in os.environ:
        docker_build_options.extend(["--builder", os.environ["BUILDER"]])
    cmd = [
        "docker",
        "build",
        "--file",
        f"Dockerfile-{odoo_version}",
        "--tag",
        f"{DEFAULT_TEST_IMAGE}:{odoo_version}-{python_tag}-{distro}-latest",
        *docker_build_options,
        ".",
    ]
    subprocess.run(cmd, check=True, cwd=HERE.parent)
    cmd = [
        "docker",
        "compose",
        "build",
        *docker_build_options,
    ]
    subprocess.run(cmd, check=True, cwd=HERE)


@pytest.fixture(scope="session")
def parsed_odoo_version(odoo_version):
    return tuple(int(x) for x in odoo_version.split("."))


@pytest.fixture(scope="session")
def compose_up(compose_build):
    subprocess.run(["docker", "compose", "up", "-d"], check=True, cwd=HERE)
    try:
        while compose_run(["pg_isready"], check=False).returncode != 0:
            time.sleep(2)
        yield
    finally:
        subprocess.run(["docker", "compose", "down"], check=True, cwd=HERE)


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
