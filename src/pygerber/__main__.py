"""Command line interface."""

from __future__ import annotations

import os
from contextlib import suppress

from pygerber.console.commands import main

if os.environ.get("COVERAGE_PROCESS_START") is not None:
    with suppress(ImportError, ModuleNotFoundError):
        import coverage

        coverage.process_startup()


if __name__ == "__main__":
    main()
