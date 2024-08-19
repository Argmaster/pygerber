"""`pygerber.gerberx3.node_visitor` contains definition of `StateTrackingVisitor`
class.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field

from pygerber.gerberx3.ast.nodes import AB, AD, AM
from pygerber.gerberx3.ast.nodes.enums import (
    AxisCorrespondence,
    CoordinateMode,
    ImagePolarity,
    Mirroring,
    Zeros,
)
from pygerber.gerberx3.ast.nodes.properties.MO import UnitMode
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr, Double, PackedCoordinateStr
from pygerber.gerberx3.ast.visitor import AstVisitor


class _StateModel(BaseModel):
    """Base class for all models representing parts of Gerber state."""


class CoordinateFormat(_StateModel):
    """Coordinate format information."""

    zeros: Zeros
    coordinate_mode: CoordinateMode

    x_integral: int
    x_decimal: int

    y_integral: int
    y_decimal: int

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if self.zeros == Zeros.SKIP_LEADING:
            self.unpack_x = self._unpack_skip_leading(self.x_integral, self.x_decimal)  # type: ignore[method-assign]
            self.unpack_y = self._unpack_skip_leading(self.y_integral, self.y_decimal)  # type: ignore[method-assign]
        elif self.zeros == Zeros.SKIP_TRAILING:
            self.unpack_x = self._unpack_skip_trailing(self.x_integral, self.x_decimal)  # type: ignore[method-assign]
            self.unpack_y = self._unpack_skip_trailing(self.y_integral, self.y_decimal)  # type: ignore[method-assign]
        else:
            msg = f"Unknown zeros mode: {self.zeros}"
            raise ValueError(msg)

    def unpack_x(self, coordinate: PackedCoordinateStr, /) -> Double:  # noqa: ARG002
        """Unpack X coordinate using the current coordinate format."""
        msg = "Coordinate format was not properly set."
        raise NotImplementedError(msg)

    def unpack_y(self, coordinate: PackedCoordinateStr, /) -> Double:  # noqa: ARG002
        """Unpack X coordinate using the current coordinate format."""
        msg = "Coordinate format was not properly set."
        raise NotImplementedError(msg)

    def _unpack_skip_trailing(
        self, integer: int, decimal: int
    ) -> Callable[[PackedCoordinateStr], Double]:
        def _(coordinate: PackedCoordinateStr) -> Double:
            padded_coordinate = coordinate.ljust((integer + decimal), "0")
            integer_value_str = padded_coordinate[:integer]
            decimal_value_str = padded_coordinate[integer:]

            return float(f"{integer_value_str}.{decimal_value_str}")

        return _

    def _unpack_skip_leading(
        self, integer: int, decimal: int
    ) -> Callable[[PackedCoordinateStr], Double]:
        def _(coordinate: PackedCoordinateStr) -> Double:
            padded_coordinate = coordinate.rjust((integer + decimal), "0")
            integer_value_str = padded_coordinate[:integer]
            decimal_value_str = padded_coordinate[integer:]

            return float(f"{integer_value_str}.{decimal_value_str}")

        return _


class Attributes(_StateModel):
    """Attributes of the Gerber file."""

    aperture_attributes: dict[str, Any] = Field(default_factory=dict)

    file_attributes: dict[str, Any] = Field(default_factory=dict)

    object_attributes: dict[str, Any] = Field(default_factory=dict)

    image_polarity: ImagePolarity = Field(default=None)
    """The name of the image. (Spec reference: 8.1.3)"""

    file_name: Optional[str] = Field(default=None)
    """The name of the file. (Spec reference: 8.1.6)"""

    axis_correspondence: AxisCorrespondence = Field(default=AxisCorrespondence.AX_BY)
    """The axis correspondence. (Spec reference: 8.1.2)"""


class Transform(_StateModel):
    """Aperture transformations."""

    mirroring: Mirroring = Field(default=Mirroring.NONE)
    """Aperture mirroring set with LM command. (Spec reference: 4.9.3)"""

    rotation: Double = Field(default=0.0)
    """Aperture rotation set with LR command. (Spec reference: 4.9.4)"""

    scaling: Double = Field(default=1.0)
    """Aperture scaling set with LS command. (Spec reference: 4.9.5)"""


class PlotMode(Enum):
    """Plot mode of the Gerber file."""

    LINEAR = "LINEAR"
    """Linear interpolation mode."""

    ARC = "ARC"
    """Clockwise circular interpolation mode."""

    CCW_ARC = "CCW_ARC"
    """Counter-clockwise circular interpolation mode."""


class ApertureStorage(_StateModel):
    """Storage for apertures."""

    apertures: dict[ApertureIdStr, AD] = Field(default_factory=dict)
    """Aperture storage."""

    blocks: dict[ApertureIdStr, AB] = Field(default_factory=dict)
    """Block aperture storage."""

    macros: dict[str, AM] = Field(default_factory=dict)
    """Macro definition storage."""


class MacroContext(_StateModel):
    """Macro evaluation context."""


class State(_StateModel):
    """Internal state of the compiler."""

    unit_mode: UnitMode = Field(default=UnitMode.METRIC)
    """The draw units used for the Gerber file. (Spec reference: 4.2.1)"""

    coordinate_format: Optional[CoordinateFormat] = Field(default=None)
    """The coordinate format specification, including the number of decimals.
    (Spec reference: 4.2.2)"""

    plot_mode: PlotMode = Field(default=PlotMode.LINEAR)
    """The plot mode. (Spec reference 4.7)"""

    current_aperture_id: Optional[ApertureIdStr] = Field(default=None)
    """The ID of currently selected aperture. (Spec reference: 8.6)"""

    current_x: Double = Field(default=0.0)
    """Current X coordinate value."""

    current_y: Double = Field(default=0.0)
    """Current Y coordinate value."""

    coordinate_x: Double = Field(default=0.0)
    """Last X coordinate value set by CoordinateX node."""

    coordinate_y: Double = Field(default=0.0)
    """Last Y coordinate value set by CoordinateY node."""

    coordinate_i: Double = Field(default=0.0)
    """Last I coordinate value set by CoordinateI node."""

    coordinate_j: Double = Field(default=0.0)
    """Last J coordinate value set by CoordinateJ node."""

    transform: Transform = Field(default_factory=lambda: Transform)
    """Current aperture transformation parameters."""

    apertures: ApertureStorage = Field(default_factory=lambda: ApertureStorage)
    """Container for different types of apertures."""

    macro_context: MacroContext = Field(default_factory=lambda: MacroContext)
    """Context used for macro evaluation."""


class StateTrackingVisitor(AstVisitor):
    """`StateTrackingVisitor` is a visitor class that tracks the internal state
    defined in the GerberX3 specification and modifies it according to Gerber
    commands.

    Additionally, it defines a set of higher level callback methods that extend
    interface of `AstVisitor` class.
    """

    def __init__(self) -> None:
        super().__init__()
        self.state = State()

    # Aperture

    def on_ab(self, node: AB) -> None:
        """Handle `ABclose` node."""
        self.state.apertures.blocks[node.open.aperture_identifier] = node

    def on_ad(self, node: AD) -> None:
        """Handle `AD` node."""
        self.state.apertures.apertures[node.aperture_identifier] = node

    def on_am(self, node: AM) -> None:
        """Handle `AM` root node."""
        self.state.apertures.macros[node.open.name] = node
