"""`vm` package contains all logic related to the virtual machines used for rendering
images with use of simple generic stateless commands.
"""

from __future__ import annotations

from typing import Any, Literal

from pygerber.vm.builder import Builder, LayerBuilder
from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.rvmc import RVMC
from pygerber.vm.vm import DeferredLayer, EagerLayer, Layer, Result, VirtualMachine

__all__ = [
    "Builder",
    "LayerBuilder",
    "RVMC",
    "VirtualMachine",
    "CommandVisitor",
    "Result",
    "Layer",
    "EagerLayer",
    "DeferredLayer",
]


def render(
    rvmc: RVMC, *, backend: Literal["pillow"] = "pillow", **options: Any
) -> Result:
    """Render RVMC code using given builder."""
    if backend == "pillow":
        from pygerber.vm.pillow import PillowVirtualMachine

        return PillowVirtualMachine(**options).run(rvmc)

    msg = f"Backend '{backend}' is not supported."  # type: ignore[unreachable]
    raise NotImplementedError(msg)
