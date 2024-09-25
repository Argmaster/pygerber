"""Main entry point of pygerber language server."""

from __future__ import annotations

import logging
import logging.config
import pathlib

import click

from pygerber.gerber.language_server.status import is_language_server_available

BUNDLE_DIR = pathlib.Path(__file__).parent.parent
logger = logging.getLogger(__name__)


@click.command(
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True}
)
@click.pass_context
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all output.",
    default=False,
)
@click.option(
    "--check-only",
    "-c",
    is_flag=True,
    help="Only check for language server availability.",
    default=False,
)
def main(ctx: click.Context, *, quiet: bool, check_only: bool) -> None:  # noqa: ARG001
    """Run main entry point for language server."""
    if check_only:
        raise SystemExit(0 if is_language_server_available() else 1)

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
    from pygerber.gerber.language_server._server.server import get_server

    server = get_server()
    server.start_io()


if __name__ == "__main__":
    main()
