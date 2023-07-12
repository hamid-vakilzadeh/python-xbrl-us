"""
Module that contains the command line app.

"""
import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main():
    """
    Args:
        argv (list): List of arguments

    Returns:
        an interface to the streamlit app.

    """
    _dir = Path(__file__).resolve()
    file_path = _dir.parent / "app.py"

    sys.argv = ["streamlit", "run", file_path.as_posix()]
    return stcli.main()
