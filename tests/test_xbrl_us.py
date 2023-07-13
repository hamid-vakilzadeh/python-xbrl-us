from pathlib import Path

from yaml import safe_load

from xbrl_us import XBRL

_dir = Path("test_xbrl_us.py").resolve()
file_path = _dir.parent / "secrets.yml"

with file_path.open("r") as file:
    credentials = safe_load(file)


def test_methods():
    xbrl = XBRL(
        username=credentials["username"],
        password=credentials["password"],
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
    )

    assert sorted(xbrl.methods())[0] == "assertion search"
