"""Main entry point of pygerber language server."""

from __future__ import annotations

import logging
import logging.config
import pathlib
import sys

from pygerber.gerberx3.language_server._internals.server import get_language_server

BUNDLE_DIR = pathlib.Path(__file__).parent.parent
logger = logging.getLogger(__name__)


def main() -> None:
    """Run main entry point for language server."""
    quiet = "--quiet" in sys.argv or "-q" in sys.argv

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {"format": "%(asctime)s %(levelname)-4s %(message)s"},
            },
            "handlers": {
                "stderr": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },
            },
            "root": {
                "level": "INFO" if not quiet else "CRITICAL",
                "handlers": ["stderr"],
            },
            "loggers": {
                # Don't repeat every message
                "pygls.protocol": {
                    "level": "WARN",
                    "handlers": ["stderr"],
                    "propagate": True,
                },
            },
        },
    )
    server = get_language_server()
    server.start_io()


if __name__ == "__main__":
    main()
