from pathlib import Path
import os
import subprocess

import pytest

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
