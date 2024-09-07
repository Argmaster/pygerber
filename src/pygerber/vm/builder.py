"""`pygerber.vm` module contains RVMC builder class."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional, Sequence

from pygerber.vm.commands import Command, Shape, StartLayer
from pygerber.vm.commands.layer import EndLayer
from pygerber.vm.commands.paste import PasteLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types import Box, LayerID, Vector
from pygerber.vm.vm import VirtualMachine


class _LayerBuilder:
    """Layer builder class."""

    def __init__(
        self,
        layer_id: LayerID,
        box: Optional[Box],
        origin: Optional[tuple[float, float]],
    ) -> None:
        self._layer_id = layer_id
        self._box = box
        self._origin = origin or Vector(x=0, y=0)
        self._active_layer_id: Optional[LayerID] = None
        self._finalized = False

        self._commands: list[Command] = [
            StartLayer(
                id=self._layer_id,
                box=box,
                origin=(
                    Vector(x=0, y=0)
                    if origin is None
                    else Vector(x=origin[0], y=origin[1])
                ),
            )
        ]

    def finalize(self) -> None:
        """Finalize the layer."""
        self._commands.append(EndLayer())
        self._finalized = True

    @contextmanager
    def layer(
        self,
        id_: str,
        box: Optional[Box] = None,
        origin: Optional[tuple[float, float]] = None,
    ) -> Generator[_LayerBuilder, None, None]:
        """Create a new layer."""
        if self._active_layer_id is not None:
            msg = "Use _LayerContext to create a nested layer."
            raise RuntimeError(msg)

        if self._finalized:
            msg = "Cannot create a new layer from finalized layer."
            raise RuntimeError(msg)

        self._active_layer_id = LayerID(id=id_)
        layer_context = _LayerBuilder(
            layer_id=self._active_layer_id, box=box, origin=origin
        )
        yield layer_context

        layer_context.finalize()
        self._commands.extend(layer_context.commands)
        self._active_layer_id = None

    @property
    def commands(self) -> Sequence[Command]:
        """Return commands."""
        return self._commands

    def circle(
        self, center: tuple[float, float], diameter: float, *, is_negative: bool
    ) -> None:
        """Add a command to the layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            Shape.new_circle(center=center, diameter=diameter, negative=is_negative)
        )

    def _check_not_finalized_in_add(self) -> None:
        if self._finalized:
            msg = "Cannot add shapes to finalized layer."
            raise RuntimeError(msg)

    def rectangle(
        self,
        center: tuple[float, float],
        width: float,
        height: float,
        *,
        is_negative: bool,
    ) -> None:
        """Add a command to the layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            Shape.new_rectangle(
                center=center, width=width, height=height, negative=is_negative
            )
        )

    def obround(
        self,
        center: tuple[float, float],
        width: float,
        height: float,
        *,
        is_negative: bool,
    ) -> None:
        """Add a command to the layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            Shape.new_obround(
                center=center, width=width, height=height, negative=is_negative
            )
        )

    def line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        thickness: float,
        *,
        is_negative: bool,
    ) -> None:
        """Add a command to the layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            Shape.new_line(
                start=start, end=end, thickness=thickness, negative=is_negative
            )
        )

    def cross(
        self,
        center: tuple[float, float],
        width: float,
        height: float,
        thickness: float,
        *,
        is_negative: bool,
    ) -> None:
        """Add cross shape to the layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            Shape.new_rectangle(
                center=center, width=width, height=thickness, negative=is_negative
            )
        )
        self._commands.append(
            Shape.new_rectangle(
                center=center, width=thickness, height=height, negative=is_negative
            )
        )

    def x(
        self,
        center: tuple[float, float],
        length: float,
        thickness: float,
        *,
        is_negative: bool,
    ) -> None:
        """Add cross shape to the layer."""
        self._check_not_finalized_in_add()
        half_length = length / 2
        self._commands.append(
            Shape.new_line(
                start=(center[0] + half_length, center[1] + half_length),
                end=(center[0] - half_length, center[1] - half_length),
                thickness=thickness,
                negative=is_negative,
            )
        )
        self._commands.append(
            Shape.new_line(
                start=(center[0] - half_length, center[1] + half_length),
                end=(center[0] + half_length, center[1] - half_length),
                thickness=thickness,
                negative=is_negative,
            )
        )

    def paste(
        self, layer: _LayerBuilder, at: tuple[float, float], *, is_negative: bool
    ) -> None:
        """Paste another layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            PasteLayer(
                source_layer_id=layer._layer_id,  # noqa: SLF001
                center=Vector.from_tuple(at),
                is_negative=is_negative,
            )
        )


class Builder:
    """RVMC builder class."""

    def __init__(self) -> None:
        self._commands: list[Command] = []

    @contextmanager
    def layer(
        self, box: Optional[Box] = None, origin: Optional[tuple[float, float]] = None
    ) -> Generator[_LayerBuilder, None, None]:
        """Create a new layer."""
        layer = _LayerBuilder(
            layer_id=VirtualMachine.MAIN_LAYER_ID, box=box, origin=origin
        )
        yield layer
        layer.finalize()
        self._commands.extend(layer.commands)

    @property
    def commands(self) -> RVMC:
        """Return commands."""
        return RVMC(commands=self._commands)
