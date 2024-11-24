from __future__ import annotations

import logging
import os
import subprocess
import sys


def test_double_under_main_file() -> None:
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "pygerber"],
        executable=sys.executable,
        env={**os.environ, "COVERAGE_PROCESS_START": ".coveragerc"},
        check=False,
        capture_output=True,
    )

    logging.info(result.stdout.decode())
    logging.error(result.stderr.decode())

    assert b"--version" in result.stdout
    assert b"--help" in result.stdout
    assert result.returncode == 0
