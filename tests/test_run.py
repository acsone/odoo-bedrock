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


def test_env_vars(odoo_version):
    cmd = []
    expected = []
    for key, value in (
        ("ODOO_BIN", "odoo"),
        ("ODOO_VERSION", odoo_version),
        ("OPENERP_SERVER", "/etc/odoo.cfg"),
        ("ODOO_RC", "/etc/odoo.cfg"),
        ("KWKHTMLTOPDF_SERVER_URL", "http://kwkhtmltopdf"),
        ("LANG", "C.UTF-8"),
        ("LC_ALL", "C.UTF-8"),
        # PG* are derived from DB_* (see entrypoint.sh and docker-compose.yml)
        ("PGUSER", "odoouser"),
        ("PGPASSWORD", "odoopassword"),
        ("PGHOST", "postgres"),
        ("PGPORT", "5432"),
        ("PGDATABASE", "odoodb"),
    ):
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
