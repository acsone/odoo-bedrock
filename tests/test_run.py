from pathlib import Path

from .testlib import compose_run


def test_run_odoo_default_command():
    result = compose_run([])
    assert "Starting with UID: 999" in result.stdout
    assert "running odoo UID=999" in result.stdout


def test_run_odoo_custom_command():
    result = compose_run(["bash", "-c", "echo 'hello world'"])
    assert "Starting with UID: 999" in result.stdout
    assert "running odoo" not in result.stdout
    assert "hello world" in result.stdout


def test_run_odoo_gosu_uid():
    result = compose_run(["bash", "-c", "echo UID=$(id -u)"])
    assert "Starting with UID: 999" in result.stdout
    assert "UID=999" in result.stdout


def test_run_odoo_gosu_custom_uid():
    result = compose_run(
        ["bash", "-c", "echo UID=$(id -u)"], env={"LOCAL_USER_ID": "888"}
    )
    assert "Starting with UID: 888" in result.stdout
    assert "UID=888" in result.stdout


def test_run_odoo_nogosu_run_as_root():
    """Test that the nogosu environment variable disables gosu."""
    result = compose_run(["bash", "-c", "echo UID=$(id -u)"], env={"NOGOSU": "1"})
    assert "Starting with UID: 999" not in result.stdout
    assert "UID=0" in result.stdout


def test_odoo_user_created_default_uid():
    result = compose_run(["bash", "-c", "echo ODOOUID=$(id -u odoo)"])
    assert "ODOOUID=999" in result.stdout


def test_odoo_user_created_custom_uid():
    result = compose_run(
        ["bash", "-c", "echo ODOOUID=$(id -u odoo)"], env={"LOCAL_USER_ID": "888"}
    )
    assert "ODOOUID=888" in result.stdout


def test_data_dirs_created():
    result = compose_run(
        ["python", "-c", "import os; print(sorted(os.listdir('/data/odoo')))"]
    )
    assert "['addons', 'filestore', 'sessions']" in result.stdout


def test_env_vars(odoo_version, parsed_odoo_version):
    env_vars = [
        ("ODOO_VERSION", odoo_version),
        ("OPENERP_SERVER", "/etc/odoo.cfg"),
        ("KWKHTMLTOPDF_SERVER_URL", "http://kwkhtmltopdf"),
        ("LANG", "C.UTF-8"),
        ("LC_ALL", "C.UTF-8"),
        # PG* are derived from DB_* (see answers.sh and docker-compose.yml)
        ("PGUSER", "odoouser"),
        ("PGPASSWORD", "odoopassword"),
        ("PGHOST", "postgres"),
        ("PGPORT", "5432"),
        ("PGDATABASE", "odoodb"),
    ]
    if parsed_odoo_version < (10, 0):
        env_vars.append(("ODOO_BIN", "openerp-server"))
    else:
        env_vars.append(("ODOO_BIN", "odoo"))
    if parsed_odoo_version >= (11, 0):
        env_vars.append(("ODOO_RC", "/etc/odoo.cfg"))
    cmd = []
    expected = []
    for key, value in env_vars:
        cmd.append(f"echo {key}=${key}")
        expected.append(f"{key}={value}")
    result = compose_run(["bash", "-c", "; ".join(cmd)])
    assert "\n".join(expected) in result.stdout


def test_run_entrypoints_default():
    result = compose_run([])
    assert "entrypoint 1 UID=999\n" in result.stdout
    assert "entrypoint 2 UID=999\n" in result.stdout


def test_run_entrypoints_nogosu():
    result = compose_run([], env={"NOGOSU": "1"})
    assert "entrypoint 1 UID=0\n" in result.stdout
    assert "entrypoint 2 UID=0\n" in result.stdout


def test_run_no_entrypoints_with_custom_cmd():
    result = compose_run(["ls"])
    assert "entrypoint 1" not in result.stdout
    assert "entrypoint 2" not in result.stdout


def test_default_odoo_cfg(odoo_version):
    expected_odoo_cfg_file = (
        Path(__file__).parent / "data" / f"expected-default-odoo-cfg-{odoo_version}.cfg"
    )
    compose_run(
        ["bash", "-c", "diff /etc/odoo.cfg /expected-odoo.cfg"],
        volumes=[f"{expected_odoo_cfg_file}:/expected-odoo.cfg"],
    )


def test_odoo_cfg_env_vars(odoo_version):
    expected_odoo_cfg_file = (
        Path(__file__).parent / "data" / f"expected-odoo-cfg-{odoo_version}.cfg"
    )
    env_vars = {
        "ADDITIONAL_ODOO_RC",
        "ADDONS_PATH",
        "ADMIN_PASSWD",
        "DB_FILTER",
        "DB_HOST",
        "DB_MAXCONN",
        "DB_NAME",
        "DB_PASSWORD",
        "DB_PORT",
        "DB_SSLMODE",
        "DB_TEMPLATE",
        "DB_USER",
        "LIMIT_MEMORY_HARD",
        "LIMIT_MEMORY_SOFT",
        "LIMIT_REQUEST",
        "LIMIT_TIME_CPU",
        "LIMIT_TIME_REAL",
        "LIMIT_TIME_REAL_CRON",
        "LIST_DB",
        "LOG_DB",
        "LOG_HANDLER",
        "LOG_LEVEL",
        "LOGFILE",
        "MAX_CRON_THREADS",
        "RUNNING_ENV",
        "SERVER_WIDE_MODULES",
        "SYSLOG",
        "UNACCENT",
        "WITHOUT_DEMO",
        "WORKERS",
    }
    env = {}
    for env_var in env_vars:
        env[env_var] = f"*{env_var}*"
    compose_run(
        ["bash", "-c", "diff /etc/odoo.cfg /expected-odoo.cfg"],
        volumes=[f"{expected_odoo_cfg_file}:/expected-odoo.cfg"],
        env=env,
    )
