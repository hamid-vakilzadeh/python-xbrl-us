"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m xbrl_us` python will execute
    ``__main__.py`` as a script. That means there will not be any
    ``xbrl_us.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there"s no ``xbrl_us.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main():
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """
    _dir = Path(__file__).resolve()
    file_path = _dir.parent / "app.py"

    sys.argv = ["streamlit", "run", file_path.as_posix()]
    return stcli.main()
