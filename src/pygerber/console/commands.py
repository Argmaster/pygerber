"""Command line commands of PyGerber."""

from __future__ import annotations

import click

import pygerber
from pygerber.console.gerber import gerber


@click.group("pygerber")
@click.version_option(version=pygerber.__version__)
def main() -> None:
    """Command line interface of PyGerber, python implementation of Gerber X3/X2
    standard with 2D rendering engine.
    """


@main.command("is-language-server-available")
def _is_language_server_available() -> None:
    from pygerber.gerber.language_server.status import is_language_server_available

    if is_language_server_available():
        click.echo("Language server is available.")
    else:
        click.echo("Language server is not available.")


main.add_command(gerber)
