from pathlib import Path
import subprocess

HERE = Path(__file__).parent


def compose_run(command, env=None, check=True):
    cmd = ["docker-compose", "run", "--rm"]
    if env:
        for key, value in env.items():
            cmd.extend(["-e", f"{key}={value}"])
    cmd.extend(["odoo"])
    cmd.extend(command)
    result = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=HERE)
    if check:
        assert result.returncode == 0, result.stderr
    return result
