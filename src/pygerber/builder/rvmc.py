"""The `pygerber.vm.builder` module provides classes for programmatic generation of
complicated RVMC.

As opposed to manual construction of RVMC by individually constructing Command objects,
builder interface is considered `stable`, hence it is guaranteed to not be modified
across patch and minor releases without previous deprecation warning.

To start building RVMC, create an instance of `Builder` class. The `Builder` class
provides a method `layer` which should be called and used as context manager.
This method will create main layer of RVMC. You can used methods on the `LayerBuilder`
instance returned by context manager to add shapes to the layer.

```python
builder = Builder()

with builder.layer() as layer:
    layer.circle((0, 0), 1, is_negative=False)

rvmc = builder.commands
```

To create a nested layer, use the `layer` method on the `LayerBuilder` instance.
Then you can proceed to add shapes to the nested layer by invoking commands
on nested layer instance. Nested layer created this way can be pasted into parent
layer using `paste` method. The `paste` method takes the nested layer instance
this explicitly disallows creation of cyclic dependencies in layers, as they will
result in exception during rendering.

```python
builder = Builder()

with builder.layer() as layer:
    with layer.layer("D10") as nested_layer:
        nested_layer.circle((0, 0), 1, is_negative=False)

    layer.paste(nested_layer, at=(0, 0), is_negative=False)

rvmc = builder.commands
```

Multiple nesting is allowed, layers defined and finalized previously can be used in any
nested layers in the future. Layers and shapes are auto-magically recorded after
corresponding method is called.

Adding shapes to finalized layer is not allowed and will result in exception.
Layers are automatically finalized after exiting the context manager corresponding
to particular layer. Before context manager is exited, eg. in nested layers, the layers
can not be used.

Using parent layer in child layer will result in cyclic dependency and will raise
exception during rendering. There is currently no mechanism preventing you from doing
that during generation.

"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional, Sequence

from pygerber.vm.commands import Command, Shape, StartLayer
from pygerber.vm.commands.layer import EndLayer
from pygerber.vm.commands.paste import PasteLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types import Box, LayerID, Vector
from pygerber.vm.vm import VirtualMachine


class RvmcBuilder:
    """The `RvmcBuilder` class provides a way to programmatically generate RVMC code."""

    def __init__(self) -> None:
        self._commands: list[Command] = []
        self._is_locked: bool = False

    @contextmanager
    def layer(
        self, box: Optional[Box] = None, origin: Optional[tuple[float, float]] = None
    ) -> Generator[LayerBuilder, None, None]:
        """Create main RVMC layer.

        Using main layer you can add more objects into the image.

        Parameters
        ----------
        box : Optional[Box], optional
            Fixed size, if not provided, size will be determined automatically at
            render time, by default None
        origin : Optional[tuple[float, float]], optional
            Origin of image space, in None, (0.0, 0.0) is used, by default None

        Yields
        ------
        Generator[LayerBuilder, None, None]
            Object allowing you to add elements to the layer.

        Raises
        ------
        LockedBuilderError
            Raised when `get_rvmc()` is called before calling this function or
            before exiting the context manager block.

        """
        if self._is_locked:
            msg = (
                "Builder was locked by calling `get_rvmc()`."
                "You need to create a new builder."
            )
            raise LockedBuilderError(msg)

        layer = LayerBuilder(
            layer_id=VirtualMachine.MAIN_LAYER_ID, box=box, origin=origin
        )
        yield layer

        layer.finalize()

        if self._is_locked:
            msg = (  # type: ignore[unreachable]
                "Builder was locked by calling `get_rvmc()` before it got finalized."
                "Do not call `get_rvmc()` before exiting `layer()` context manager "
                "block. You need to create a new builder."
            )
            raise LockedBuilderError(msg)

        self._commands.extend(layer.commands)

    def get_rvmc(self) -> RVMC:
        """Return the generated RVMC code."""
        self._is_locked = True
        return RVMC(commands=self._commands)


class LayerBuilder:
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
    ) -> Generator[LayerBuilder, None, None]:
        """Create a new layer."""
        if self._active_layer_id is not None:
            msg = "Use _LayerContext to create a nested layer."
            raise RuntimeError(msg)

        if self._finalized:
            msg = "Cannot create a new layer from finalized layer."
            raise RuntimeError(msg)

        self._active_layer_id = LayerID(id=id_)
        layer_context = LayerBuilder(
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
            Shape.new_circle(center=center, diameter=diameter, is_negative=is_negative)
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
                center=center, width=width, height=height, is_negative=is_negative
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
                center=center, width=width, height=height, is_negative=is_negative
            )
        )

    def polygon(
        self,
        center: tuple[float, float],
        outer_diameter: float,
        vertices_count: int,
        base_rotation: float,
        *,
        is_negative: bool,
    ) -> None:
        """Add Shape object containing a regular polygon inscribed in bounding_circle
        of diameter `outer_diameter`, with vertices count equal to `vertices_count`,
        and starting rotation (counterclockwise) of `base_rotation` degrees.

        Parameters
        ----------
        center : tuple[float, float]
            Center of the polygon. A tuple of two floats.
        outer_diameter : float
            Diameter of the circle circumscribing the regular polygon, i.e.
            the circle through the polygon vertices. A decimal > 0.
        vertices_count : int
            Number of vertices n, 3 ≤ n ≤ 12. An integer.
        base_rotation : float
            The rotation angle, in degrees counterclockwise. A decimal.
            With rotation angle zero there is a vertex on the positive X-axis
            through the aperture center.
        is_negative : bool
            Toggle switch for the negative polarity. If True, the aperture is
            considered solid, otherwise a hole, possibly subtracting from existing
            solid shapes.

        """
        self._check_not_finalized_in_add()
        self._commands.append(
            Shape.new_polygon(
                center=center,
                outer_diameter=outer_diameter,
                vertices_count=vertices_count,
                base_rotation=base_rotation,
                is_negative=is_negative,
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
                start=start, end=end, thickness=thickness, is_negative=is_negative
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
                center=center, width=width, height=thickness, is_negative=is_negative
            )
        )
        self._commands.append(
            Shape.new_rectangle(
                center=center, width=thickness, height=height, is_negative=is_negative
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
                is_negative=is_negative,
            )
        )
        self._commands.append(
            Shape.new_line(
                start=(center[0] - half_length, center[1] + half_length),
                end=(center[0] + half_length, center[1] - half_length),
                thickness=thickness,
                is_negative=is_negative,
            )
        )

    def paste(
        self, layer: LayerBuilder, at: tuple[float, float], *, is_negative: bool
    ) -> None:
        """Paste another layer into this layer."""
        self._check_not_finalized_in_add()
        self._commands.append(
            PasteLayer(
                source_layer_id=layer._layer_id,  # noqa: SLF001
                center=Vector.from_tuple(at),
                is_negative=is_negative,
            )
        )


class LockedBuilderError(Exception):
    """Exception raised when trying to modify a builder after it produced RVMC."""
