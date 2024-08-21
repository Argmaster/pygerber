"""`pygerber.gerberx3.node_visitor` contains definition of `StateTrackingVisitor`
class.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field

from pygerber.common.error import throw
from pygerber.gerberx3.ast.errors import (
    ApertureNotFoundError,
    ApertureNotSelectedError,
    DirectADHandlerDispatchNotSupportedError,
)
from pygerber.gerberx3.ast.nodes import (
    AB,
    AD,
    ADC,
    ADO,
    ADP,
    ADR,
    AM,
    D01,
    D02,
    D03,
    G01,
    G02,
    G03,
    TA,
    TD,
    TF,
    TO,
    ADmacro,
    ApertureIdStr,
    Dnn,
    Double,
    PackedCoordinateStr,
)
from pygerber.gerberx3.ast.nodes.enums import (
    AxisCorrespondence,
    CoordinateMode,
    ImagePolarity,
    Mirroring,
    UnitMode,
    Zeros,
)
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

    aperture_attributes: dict[str, TA] = Field(default_factory=dict)
    """Object attributes created with TA extended command."""

    file_attributes: dict[str, TF] = Field(default_factory=dict)
    """Object attributes created with TF extended command."""

    object_attributes: dict[str, TO] = Field(default_factory=dict)
    """Object attributes created with TO extended command."""

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

    coordinate_x: Optional[Double] = Field(default=None)
    """Last X coordinate value set by CoordinateX node."""

    coordinate_y: Optional[Double] = Field(default=None)
    """Last Y coordinate value set by CoordinateY node."""

    coordinate_i: Optional[Double] = Field(default=None)
    """Last I coordinate value set by CoordinateI node."""

    coordinate_j: Optional[Double] = Field(default=None)
    """Last J coordinate value set by CoordinateJ node."""

    transform: Transform = Field(default_factory=Transform)
    """Current aperture transformation parameters."""

    apertures: ApertureStorage = Field(default_factory=ApertureStorage)
    """Container for different types of apertures."""

    macro_context: MacroContext = Field(default_factory=MacroContext)
    """Context used for macro evaluation."""

    attributes: Attributes = Field(default_factory=Attributes)
    """Container for holding currently active attributes."""

    @property
    def current_aperture(self) -> AD | AB:
        """Get currently selected aperture."""
        if self.current_aperture_id is None:
            raise ApertureNotSelectedError

        if self.current_aperture_id in self.apertures.apertures:
            return self.apertures.apertures[self.current_aperture_id]

        if self.current_aperture_id in self.apertures.blocks:
            return self.apertures.blocks[self.current_aperture_id]

        raise ApertureNotFoundError(self.current_aperture_id)


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
        self._on_d01_handler = self.on_draw_line
        self._on_d03_handler_dispatch_table = {
            AD: lambda *_: throw(DirectADHandlerDispatchNotSupportedError()),
            ADC: self.on_flash_circle,
            ADR: self.on_flash_rectangle,
            ADO: self.on_flash_obround,
            ADP: self.on_flash_polygon,
            ADmacro: self.on_flash_macro,
            AB: self.on_flash_block,
        }
        self._on_d03_handler: Callable[[D03, AD | AB], None] = lambda *_: throw(  # type: ignore[unreachable]
            ApertureNotSelectedError()
        )

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

    # Attribute

    def on_ta(self, node: TA) -> None:
        """Handle `TA_UserName` node."""
        self.state.attributes.aperture_attributes[node.attribute_name] = node

    def on_tf(self, node: TF) -> None:
        """Handle `TF` node."""
        self.state.attributes.file_attributes[node.attribute_name] = node

    def on_to(self, node: TO) -> None:
        """Handle `TO` node."""
        self.state.attributes.object_attributes[node.attribute_name] = node

    def on_td(self, node: TD) -> None:
        """Handle `TD` node."""
        if node.name is None:
            self.state.attributes.aperture_attributes.clear()
            self.state.attributes.object_attributes.clear()
            return

        self.state.attributes.aperture_attributes.pop(node.name, None)
        self.state.attributes.object_attributes.pop(node.name, None)

    def on_d01(self, node: D01) -> None:
        """Handle `D01` node."""
        super().on_d01(node)
        self._on_d01_handler(node)
        self._update_coordinates()

    def on_draw_line(self, node: D01) -> None:
        """Handle `D01` node in linear interpolation mode."""

    def on_draw_cw_arc(self, node: D01) -> None:
        """Handle `D01` node in clockwise circular interpolation mode."""

    def on_draw_ccw_arc(self, node: D01) -> None:
        """Handle `D01` node in counter-clockwise circular interpolation."""

    def _update_coordinates(self) -> None:
        if self.state.coordinate_x is not None:
            self.state.current_x = self.state.coordinate_x
        if self.state.coordinate_y is not None:
            self.state.current_y = self.state.coordinate_y

    def on_d02(self, node: D02) -> None:
        """Handle `D02` node."""
        super().on_d02(node)
        self._update_coordinates()

    def on_d03(self, node: D03) -> None:
        """Handle `D03` node."""
        super().on_d03(node)
        self._on_d03_handler(node, self._current_aperture)
        self._update_coordinates()

    def on_flash_circle(self, node: D03, aperture: ADC) -> None:
        """Handle `D03` node with `ADC` aperture."""

    def on_flash_rectangle(self, node: D03, aperture: ADR) -> None:
        """Handle `D03` node with `ADR` aperture."""

    def on_flash_obround(self, node: D03, aperture: ADO) -> None:
        """Handle `D03` node with `ADO` aperture."""

    def on_flash_polygon(self, node: D03, aperture: ADP) -> None:
        """Handle `D03` node with `ADP` aperture."""

    def on_flash_macro(self, node: D03, aperture: ADmacro) -> None:
        """Handle `D03` node with `ADM` aperture."""

    def on_flash_block(self, node: D03, aperture: AB) -> None:
        """Handle `D03` node with `AB` aperture."""

    def on_dnn(self, node: Dnn) -> None:
        """Handle `Dnn` node."""
        self.state.current_aperture_id = node.aperture_id
        self._current_aperture = self.state.current_aperture
        self._on_d03_handler = self._on_d03_handler_dispatch_table[  # type: ignore[assignment]
            type(self._current_aperture)
        ]

    # G codes

    def on_g01(self, node: G01) -> None:
        """Handle `G01` node."""
        super().on_g01(node)
        self._on_d01_handler = self.on_draw_line

    def on_g02(self, node: G02) -> None:
        """Handle `G02` node."""
        super().on_g02(node)
        self._on_d01_handler = self.on_draw_cw_arc

    def on_g03(self, node: G03) -> None:
        """Handle `G03` node."""
        super().on_g03(node)
        self._on_d01_handler = self.on_draw_ccw_arc
