# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

from .cli import handle_pygerber_cli


def main():
    handle_pygerber_cli(sys.argv[1:])


if __name__ == "__main__":
    main()
