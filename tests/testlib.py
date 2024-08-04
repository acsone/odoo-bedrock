from pathlib import Path
import os
import subprocess

HERE = Path(__file__).parent


def odoo_version():
    # /!\ Default must be the same as the ODOOVERSION build arg in test Dockerfile
    return os.environ.get("ODOOVERSION", "16.0")


def parsed_odoo_version():
    return tuple(int(x) for x in odoo_version().split("."))


def compose_run(command, env=None, check=True, volumes=None):
    cmd = ["docker", "compose", "run", "--rm"]
    if env:
        for key, value in env.items():
            cmd.extend(["-e", f"{key}={value}"])
    if volumes:
        for volume in volumes:
            cmd.extend(["-v", volume])
    cmd.extend(["odoo"])
    cmd.extend(command)
    result = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=HERE)
    if check:
        assert result.returncode == 0, result.stderr + "\n" + result.stdout
    return result
