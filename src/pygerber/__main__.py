# -*- coding: utf-8 -*-
"""
Entrypoint module for PyGerber command line interface.
Type following to invoke:
python -m pygerber
"""

import sys

from .cli import handle_pygerber_cli


def main():
    handle_pygerber_cli(sys.argv[1:])


if __name__ == "__main__":
    main()
