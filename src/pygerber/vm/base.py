"""`base` module contains definition of base `VirtualMachine` class."""

from __future__ import annotations

from typing import Sequence

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands.command import Command


class Result:
    """Result of drawing."""


class VirtualMachine(CommandVisitor):
    """Virtual machine for executing simple drawing commands."""

    def run(self, commands: Sequence[Command]) -> Result:
        """Execute all commands."""
        for command in commands:
            command.visit(self)

        return Result()
