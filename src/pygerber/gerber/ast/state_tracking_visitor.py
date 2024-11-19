"""The `state_tracking_visitor` module contains definition of
`StateTrackingVisitor` class.
"""

from __future__ import annotations

from contextlib import suppress
from enum import Enum
from itertools import chain
from typing import Any, Callable, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from pygerber.common.error import throw
from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.errors import (
    ApertureNotFoundError,
    ApertureNotSelectedError,
    CoordinateFormatNotSetError,
    DirectADHandlerDispatchNotSupportedError,
    PackedCoordinateTooLongError,
    PackedCoordinateTooShortError,
)
from pygerber.gerber.ast.nodes import (
    AB,
    AD,
    ADC,
    ADO,
    ADP,
    ADR,
    AM,
    AS,
    D01,
    D02,
    D03,
    FS,
    G01,
    G02,
    G03,
    G36,
    G37,
    G70,
    G71,
    G74,
    G75,
    G90,
    G91,
    IN,
    IP,
    IR,
    LM,
    LN,
    LP,
    LR,
    LS,
    M00,
    M02,
    MI,
    MO,
    OF,
    SF,
    TA,
    TD,
    TF,
    TO,
    ADmacro,
    ApertureIdStr,
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
    Dnn,
    Double,
    File,
    PackedCoordinateStr,
)
from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import (
    AxisCorrespondence,
    CoordinateNotation,
    ImagePolarity,
    Mirroring,
    Polarity,
    UnitMode,
    Zeros,
)


class _StateModel(BaseModel):
    """Base class for all models representing parts of Gerber state."""

    model_config = ConfigDict(
        extra="allow",
        frozen=False,
        arbitrary_types_allowed=True,
    )


class CoordinateFormat(_StateModel):
    """Coordinate format information."""

    zeros: Zeros = Field(default=Zeros.SKIP_LEADING)
    coordinate_mode: CoordinateNotation = Field(default=CoordinateNotation.ABSOLUTE)

    x_integral: int = Field(default=2)
    x_decimal: int = Field(default=6)

    y_integral: int = Field(default=2)
    y_decimal: int = Field(default=6)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if self.zeros in (Zeros.SKIP_LEADING, Zeros.SKIP_LEADING_IMPLIED):
            self.unpack_x = self._unpack_skip_leading(self.x_integral, self.x_decimal)  # type: ignore[method-assign]
            self.unpack_y = self._unpack_skip_leading(self.y_integral, self.y_decimal)  # type: ignore[method-assign]
            self.pack_x = self._pack_skip_leading(self.x_integral, self.x_decimal)  # type: ignore[method-assign]
            self.pack_y = self._pack_skip_leading(self.y_integral, self.y_decimal)  # type: ignore[method-assign]
        elif self.zeros == Zeros.SKIP_TRAILING:
            self.unpack_x = self._unpack_skip_trailing(self.x_integral, self.x_decimal)  # type: ignore[method-assign]
            self.unpack_y = self._unpack_skip_trailing(self.y_integral, self.y_decimal)  # type: ignore[method-assign]
            self.pack_x = self._pack_skip_trailing(self.x_integral, self.x_decimal)  # type: ignore[method-assign]
            self.pack_y = self._pack_skip_trailing(self.y_integral, self.y_decimal)  # type: ignore[method-assign]
        else:
            msg = f"Unknown zeros mode: {self.zeros}"  # type: ignore[unreachable]
            raise ValueError(msg)

    def unpack_x(self, coordinate: PackedCoordinateStr, /) -> Double:
        """Unpack X coordinate using the current coordinate format."""
        msg = "Coordinate format was not properly set."
        raise NotImplementedError(msg)  # pragma: no cover

    def unpack_y(self, coordinate: PackedCoordinateStr, /) -> Double:
        """Unpack X coordinate using the current coordinate format."""
        msg = "Coordinate format was not properly set."
        raise NotImplementedError(msg)  # pragma: no cover

    def _unpack_skip_trailing(
        self, integer: int, decimal: int
    ) -> Callable[[PackedCoordinateStr], Double]:
        def _(coordinate: PackedCoordinateStr) -> Double:
            sign, coordinate_str = self._unpack_preprocess(coordinate, integer, decimal)

            padded_coordinate = coordinate_str.ljust((integer + decimal), "0")
            integer_value_str = padded_coordinate[:integer]
            decimal_value_str = padded_coordinate[integer:]

            return float(f"{sign}{integer_value_str}.{decimal_value_str}")

        return _

    def _unpack_skip_leading(
        self, integer: int, decimal: int
    ) -> Callable[[PackedCoordinateStr], Double]:
        def _(coordinate: PackedCoordinateStr) -> Double:
            sign, coordinate_str = self._unpack_preprocess(coordinate, integer, decimal)

            padded_coordinate = coordinate_str.rjust((integer + decimal), "0")
            integer_value_str = padded_coordinate[:integer]
            decimal_value_str = padded_coordinate[integer:]

            return float(f"{sign}{integer_value_str}.{decimal_value_str}")

        return _

    def _unpack_preprocess(
        self, coordinate: PackedCoordinateStr, integer: int, decimal: int
    ) -> tuple[Literal["-", "+"], str]:
        if len(coordinate) <= 0:
            raise PackedCoordinateTooShortError(coordinate, integer, decimal)

        sign: Literal["+", "-"] = "+"

        if coordinate[0] in ("+", "-"):
            sign = coordinate[0]  # type: ignore[assignment]
            coordinate_str = coordinate[1:]
        else:
            coordinate_str = str(coordinate)

        if len(coordinate_str) > (integer + decimal):
            raise PackedCoordinateTooLongError(coordinate, integer, decimal)

        if len(coordinate_str) <= 0:
            raise PackedCoordinateTooShortError(coordinate, integer, decimal)

        return sign, coordinate_str

    def pack_x(self, coordinate: Double, /) -> PackedCoordinateStr:
        """Unpack X coordinate using the current coordinate format."""
        msg = "Coordinate format was not properly set."
        raise NotImplementedError(msg)  # pragma: no cover

    def pack_y(self, coordinate: Double, /) -> PackedCoordinateStr:
        """Pack X coordinate using the current coordinate format."""
        msg = "Coordinate format was not properly set."
        raise NotImplementedError(msg)  # pragma: no cover

    def _pack_skip_leading(
        self,
        integer: int,
        decimal: int,
    ) -> Callable[[Double], PackedCoordinateStr]:
        def _(coordinate: Double) -> PackedCoordinateStr:
            integer_str, decimal_str = f"{coordinate:.{decimal}f}".split(".")
            assert len(integer_str) > 0
            assert len(decimal_str) > 0

            if integer_str[0] in ("+", "-"):
                sign, integer_str = integer_str[0], integer_str[1:]
            else:
                sign = ""

            if len(integer_str) > integer:
                raise PackedCoordinateTooLongError(str(coordinate), integer, decimal)

            packed_no_sign = f"{integer_str}{decimal_str}".lstrip("0") or "0"

            return PackedCoordinateStr(f"{sign}{packed_no_sign}")

        return _

    def _pack_skip_trailing(
        self,
        integer: int,
        decimal: int,
    ) -> Callable[[Double], PackedCoordinateStr]:
        def _(coordinate: Double) -> PackedCoordinateStr:
            integer_str, decimal_str = f"{coordinate:.{decimal}f}".split(".")
            assert len(integer_str) > 0
            assert len(decimal_str) > 0

            if integer_str[0] in ("+", "-"):
                sign, integer_str = integer_str[0], integer_str[1:]
            else:
                sign = ""

            if len(integer_str) > integer:
                raise PackedCoordinateTooLongError(str(coordinate), integer, decimal)

            integer_str = integer_str.rjust(integer, "0")

            packed_no_sign = f"{integer_str}{decimal_str}".rstrip("0") or "0"

            return PackedCoordinateStr(f"{sign}{packed_no_sign}")

        return _


class Attributes(_StateModel):
    """Attributes Gerber X3 of apertures, objects and file."""

    aperture_attributes: Dict[str, TA] = Field(default_factory=dict)
    """Object attributes created with TA extended command."""

    file_attributes: Dict[str, TF] = Field(default_factory=dict)
    """Object attributes created with TF extended command."""

    object_attributes: Dict[str, TO] = Field(default_factory=dict)
    """Object attributes created with TO extended command."""


class ImageAttributes(_StateModel):
    """Legacy attributes of the image."""

    polarity: ImagePolarity = Field(default=None)
    """The name of the image. (Spec reference: 8.1.4)"""

    rotation: Double = Field(default=0.0)
    """The rotation of the image. (Spec reference: 8.1.5)"""

    a_axis_mirroring: int = Field(default=0)
    """The mirroring of A axis of the image. (Spec reference: 8.1.7)"""

    b_axis_mirroring: int = Field(default=0)
    """The mirroring of B axis of the image. (Spec reference: 8.1.7)"""

    a_axis_offset: Optional[Double] = Field(default=0)
    """The offset of A axis of the image. (Spec reference: 8.1.8)"""

    b_axis_offset: Optional[Double] = Field(default=0)
    """The offset of B axis of the image. (Spec reference: 8.1.8)"""

    a_axis_scale: Optional[Double] = Field(default=0)
    """The scale of A axis of the image. (Spec reference: 8.1.9)"""

    b_axis_scale: Optional[Double] = Field(default=0)
    """The scale of B axis of the image. (Spec reference: 8.1.9)"""

    image_name: Optional[str] = Field(default=None)
    """The name of the image. (Spec reference: 8.1.3)"""

    file_name: Optional[str] = Field(default=None)
    """The name of the file. (Spec reference: 8.1.6)"""

    axis_correspondence: AxisCorrespondence = Field(default=AxisCorrespondence.AX_BY)
    """The axis correspondence. (Spec reference: 8.1.2)"""


class Transform(_StateModel):
    """Aperture transformations."""

    polarity: Polarity = Field(default=Polarity.Dark)
    """Aperture polarity set with LP command. (Spec reference: 4.9.2)"""

    mirroring: Mirroring = Field(default=Mirroring.NONE)
    """Aperture mirroring set with LM command. (Spec reference: 4.9.3)"""

    rotation: Double = Field(default=0.0)
    """Aperture rotation set with LR command. (Spec reference: 4.9.4)"""

    scaling: Double = Field(default=1.0)
    """Aperture scaling set with LS command. (Spec reference: 4.9.5)"""

    @property
    def tag(self) -> str:
        """Get string tag identifying the transformation."""
        return f"{self.mirroring.value}%{self.rotation:.8f}%{self.scaling:.8f}"


class PlotMode(Enum):
    """Plot mode of the Gerber file."""

    LINEAR = "LINEAR"
    """Linear interpolation mode."""

    ARC = "ARC"
    """Clockwise circular interpolation mode."""

    CCW_ARC = "CCW_ARC"
    """Counter-clockwise circular interpolation mode."""


class ArcInterpolation(Enum):
    """Arc interpolation mode."""

    SINGLE_QUADRANT = "SINGLE_QUADRANT"
    """Single quadrant mode."""

    MULTI_QUADRANT = "MULTI_QUADRANT"
    """Multi quadrant mode."""


class ApertureStorage(_StateModel):
    """Storage for apertures."""

    apertures: Dict[ApertureIdStr, AD] = Field(default_factory=dict)
    """Aperture storage."""

    blocks: Dict[ApertureIdStr, AB] = Field(default_factory=dict)
    """Block aperture storage."""

    macros: Dict[str, AM] = Field(default_factory=dict)
    """Macro definition storage."""

    per_aperture_attributes: Dict[str, Dict[str, TA]] = Field(default_factory=dict)
    """Attributes assigned to apertures during creation."""

    def get_next_free_aperture_code(self) -> int:
        """Get next free aperture code."""
        return (
            max(
                int(aperture_id.lstrip("D"))
                for aperture_id in chain(self.apertures.keys(), self.blocks.keys())
            )
            + 1
        )


class State(_StateModel):
    """Internal state of the compiler."""

    unit_mode: UnitMode = Field(default=UnitMode.METRIC)
    """The draw units used for the Gerber file. (Spec reference: 4.2.1)"""

    coordinate_format: Optional[CoordinateFormat] = Field(default=None)
    """The coordinate format specification, including the number of decimals.
    (Spec reference: 4.2.2)"""

    plot_mode: PlotMode = Field(default=PlotMode.LINEAR)
    """The plot mode. (Spec reference 4.7)"""

    arc_interpolation: ArcInterpolation = Field(
        default=ArcInterpolation.SINGLE_QUADRANT
    )
    """The arc interpolation mode. (Spec reference: 4.7.2)"""

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

    attributes: Attributes = Field(default_factory=Attributes)
    """Container for holding currently active attributes."""

    image_attributes: ImageAttributes = Field(default_factory=ImageAttributes)
    """Container for holding legacy image attributes."""

    is_region: bool = Field(default=False)
    """Flag indicating if visitor is in region mode."""

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


class ProgramStop(Exception):  # noqa: N818
    """Exception raised when M00 or M02 command is encountered."""

    def __init__(self, node: M00 | M02) -> None:
        self.node = node
        super().__init__()


class StateTrackingVisitor(AstVisitor):
    """`StateTrackingVisitor` is a visitor class that tracks the internal state
    defined in the Gerber X3 specification and modifies it according to Gerber
    commands.

    Additionally, it defines a set of higher level callback methods that extend
    interface of `AstVisitor` class.
    """

    def __init__(self, *, ignore_program_stop: bool = False) -> None:
        super().__init__()
        self._ignore_program_stop = ignore_program_stop

        self.state = State()
        self._on_d01_handler = self.on_draw_line
        self._plot_mode_to_d01_handler = {
            PlotMode.LINEAR: {
                ArcInterpolation.SINGLE_QUADRANT: self.on_draw_line,
                ArcInterpolation.MULTI_QUADRANT: self.on_draw_line,
            },
            PlotMode.ARC: {
                ArcInterpolation.SINGLE_QUADRANT: self.on_draw_cw_arc_sq,
                ArcInterpolation.MULTI_QUADRANT: self.on_draw_cw_arc_mq,
            },
            PlotMode.CCW_ARC: {
                ArcInterpolation.SINGLE_QUADRANT: self.on_draw_ccw_arc_sq,
                ArcInterpolation.MULTI_QUADRANT: self.on_draw_ccw_arc_mq,
            },
        }
        self._plot_mode_to_in_region_d01_handler = {
            PlotMode.LINEAR: {
                ArcInterpolation.SINGLE_QUADRANT: self.on_in_region_draw_line,
                ArcInterpolation.MULTI_QUADRANT: self.on_in_region_draw_line,
            },
            PlotMode.ARC: {
                ArcInterpolation.SINGLE_QUADRANT: self.on_in_region_draw_cw_arc_sq,
                ArcInterpolation.MULTI_QUADRANT: self.on_in_region_draw_cw_arc_mq,
            },
            PlotMode.CCW_ARC: {
                ArcInterpolation.SINGLE_QUADRANT: self.on_in_region_draw_ccw_arc_sq,
                ArcInterpolation.MULTI_QUADRANT: self.on_in_region_draw_ccw_arc_mq,
            },
        }
        self._on_d03_handler: Callable[[D03, AD | AB], None] = lambda *_: throw(  # type: ignore[unreachable]
            ApertureNotSelectedError()
        )
        self._dispatch_d01_handler: Callable[[], None] = (
            self._dispatch_d01_handler_non_region
        )

    @property
    def coordinate_x(self) -> Double:
        """Get X coordinate."""
        coordinate = self.state.coordinate_x
        if coordinate is None:
            return self.state.current_x
        return coordinate

    @property
    def coordinate_y(self) -> Double:
        """Get Y coordinate."""
        coordinate = self.state.coordinate_y
        if coordinate is None:
            return self.state.current_y
        return coordinate

    @property
    def coordinate_i(self) -> Double:
        """Get X coordinate."""
        coordinate = self.state.coordinate_i
        if coordinate is None:
            return 0.0
        return coordinate

    @property
    def coordinate_j(self) -> Double:
        """Get Y coordinate."""
        coordinate = self.state.coordinate_j
        if coordinate is None:
            return 0.0
        return coordinate

    @property
    def is_negative(self) -> bool:
        """Check if current aperture is negative."""
        return self.state.transform.polarity == Polarity.Clear

    # Aperture

    def on_ab(self, node: AB) -> AB:
        """Handle `AB` node."""
        super().on_ab(node)
        self.state.apertures.blocks[node.open.aperture_id] = node
        self.state.apertures.per_aperture_attributes[node.open.aperture_id] = (
            self.state.attributes.aperture_attributes.copy()
        )
        return node

    def on_ad(self, node: AD) -> None:
        """Handle `AD` node."""
        self.state.apertures.apertures[node.aperture_id] = node
        self.state.apertures.per_aperture_attributes[node.aperture_id] = (
            self.state.attributes.aperture_attributes.copy()
        )

    def on_am(self, node: AM) -> AM:
        """Handle `AM` root node."""
        self.state.apertures.macros[node.open.name] = node
        return node

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

    def on_td(self, node: TD) -> TD:
        """Handle `TD` node."""
        if node.name is None:
            self.state.attributes.aperture_attributes.clear()
            self.state.attributes.object_attributes.clear()
            return node

        self.state.attributes.aperture_attributes.pop(node.name, None)
        self.state.attributes.object_attributes.pop(node.name, None)
        return node

    def on_d01(self, node: D01) -> D01:
        """Handle `D01` node."""
        super().on_d01(node)
        self._on_d01_handler(node)
        self._update_coordinates()
        return node

    def on_draw_line(self, node: D01) -> None:
        """Handle `D01` node in linear interpolation mode."""

    def on_draw_cw_arc_sq(self, node: D01) -> None:
        """Handle `D01` node in clockwise circular interpolation single quadrant
        mode.
        """

    def on_draw_cw_arc_mq(self, node: D01) -> None:
        """Handle `D01` node in clockwise circular interpolation multi quadrant mode."""

    def on_draw_ccw_arc_sq(self, node: D01) -> None:
        """Handle `D01` node in counter-clockwise circular interpolation single quadrant
        mode.
        """

    def on_draw_ccw_arc_mq(self, node: D01) -> None:
        """Handle `D01` node in counter-clockwise circular interpolation multi quadrant
        mode.
        """

    def _update_coordinates(self) -> None:
        if self.state.coordinate_x is not None:
            self.state.current_x = self.state.coordinate_x
        if self.state.coordinate_y is not None:
            self.state.current_y = self.state.coordinate_y

    def on_d02(self, node: D02) -> D02:
        """Handle `D02` node."""
        super().on_d02(node)
        self._update_coordinates()
        if self.state.is_region:
            self.on_flush_region()
        return node

    def on_d03(self, node: D03) -> D03:
        """Handle `D03` node."""
        super().on_d03(node)
        self._on_d03_handler(node, self.state.current_aperture)
        self._update_coordinates()
        return node

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

    def on_dnn(self, node: Dnn) -> Dnn:
        """Handle `Dnn` node."""
        self.state.current_aperture_id = node.aperture_id

        aperture = self.state.current_aperture
        handler: Any

        if isinstance(aperture, ADC):
            handler = self.on_flash_circle
        elif isinstance(aperture, ADR):
            handler = self.on_flash_rectangle
        elif isinstance(aperture, ADO):
            handler = self.on_flash_obround
        elif isinstance(aperture, ADP):
            handler = self.on_flash_polygon
        elif isinstance(aperture, ADmacro):
            handler = self.on_flash_macro
        elif isinstance(aperture, AB):
            handler = self.on_flash_block
        elif isinstance(aperture, AD):
            raise DirectADHandlerDispatchNotSupportedError

        self._on_d03_handler = handler
        return node

    # G codes

    def on_g01(self, node: G01) -> G01:
        """Handle `G01` node."""
        super().on_g01(node)
        self.state.plot_mode = PlotMode.LINEAR
        self._dispatch_d01_handler()
        return node

    def _dispatch_d01_handler_in_region(self) -> None:
        self._on_d01_handler = self._plot_mode_to_in_region_d01_handler[
            self.state.plot_mode
        ][self.state.arc_interpolation]

    def _dispatch_d01_handler_non_region(self) -> None:
        self._on_d01_handler = self._plot_mode_to_d01_handler[self.state.plot_mode][
            self.state.arc_interpolation
        ]

    def on_g02(self, node: G02) -> G02:
        """Handle `G02` node."""
        super().on_g02(node)
        self.state.plot_mode = PlotMode.ARC
        self._dispatch_d01_handler()
        return node

    def on_g03(self, node: G03) -> G03:
        """Handle `G03` node."""
        super().on_g03(node)
        self.state.plot_mode = PlotMode.CCW_ARC
        self._dispatch_d01_handler()
        return node

    def on_g36(self, node: G36) -> G36:
        """Handle `G36` node."""
        super().on_g36(node)
        self.on_start_region()
        return node

    def on_start_region(self) -> None:
        """Handle start of region."""
        self.state.is_region = True
        self._dispatch_d01_handler = self._dispatch_d01_handler_in_region
        self._dispatch_d01_handler()

    def on_in_region_draw_line(self, node: D01) -> None:
        """Handle `D01` node in linear interpolation mode in region."""

    def on_in_region_draw_cw_arc_sq(self, node: D01) -> None:
        """Handle `D01` node in clockwise circular interpolation single quadrant mode
        within region statement.
        """

    def on_in_region_draw_cw_arc_mq(self, node: D01) -> None:
        """Handle `D01` node in clockwise circular interpolation multi quadrant mode
        within region statement.
        """

    def on_in_region_draw_ccw_arc_sq(self, node: D01) -> None:
        """Handle `D01` node in counter-clockwise circular interpolation single quadrant
        mode within region statement.
        """

    def on_in_region_draw_ccw_arc_mq(self, node: D01) -> None:
        """Handle `D01` node in counter-clockwise circular interpolation multi quadrant
        mode within region statement.
        """

    def on_g37(self, node: G37) -> G37:
        """Handle `G37` node."""
        super().on_g37(node)
        self.on_flush_region()
        self.on_end_region()
        return node

    def on_flush_region(self) -> None:
        """Handle flush region after D02 command or after G37."""

    def on_end_region(self) -> None:
        """Handle end of region."""
        self.state.is_region = False
        self._dispatch_d01_handler = self._dispatch_d01_handler_non_region
        self._dispatch_d01_handler()

    def on_g70(self, node: G70) -> G70:
        """Handle `G70` node."""
        super().on_g70(node)
        self.state.unit_mode = UnitMode.IMPERIAL
        return node

    def on_g71(self, node: G71) -> G71:
        """Handle `G71` node."""
        super().on_g71(node)
        self.state.unit_mode = UnitMode.METRIC
        return node

    def on_g74(self, node: G74) -> G74:
        """Handle `G74` node."""
        super().on_g74(node)
        self.state.arc_interpolation = ArcInterpolation.SINGLE_QUADRANT
        self._dispatch_d01_handler()
        return node

    def on_g75(self, node: G75) -> G75:
        """Handle `G75` node."""
        super().on_g75(node)
        self.state.arc_interpolation = ArcInterpolation.MULTI_QUADRANT
        self._dispatch_d01_handler()
        return node

    def on_g90(self, node: G90) -> G90:
        """Handle `G90` node."""
        super().on_g90(node)
        if self.state.coordinate_format is None:
            self.state.coordinate_format = CoordinateFormat()

        self.state.coordinate_format.coordinate_mode = CoordinateNotation.ABSOLUTE
        return node

    def on_g91(self, node: G91) -> G91:
        """Handle `G91` node."""
        super().on_g91(node)
        if self.state.coordinate_format is None:
            self.state.coordinate_format = CoordinateFormat()

        self.state.coordinate_format.coordinate_mode = CoordinateNotation.INCREMENTAL
        return node

    def on_lm(self, node: LM) -> LM:
        """Handle `LM` node."""
        super().on_lm(node)
        self.state.transform.mirroring = node.mirroring
        return node

    def on_ln(self, node: LN) -> LN:
        """Handle `LN` node."""
        super().on_ln(node)
        self.state.image_attributes.file_name = node.name
        return node

    def on_lp(self, node: LP) -> LP:
        """Handle `LP` node."""
        super().on_lp(node)
        self.state.transform.polarity = node.polarity
        return node

    def on_lr(self, node: LR) -> LR:
        """Handle `LR` node."""
        super().on_lr(node)
        self.state.transform.rotation = node.rotation
        return node

    def on_ls(self, node: LS) -> LS:
        """Handle `LS` node."""
        super().on_ls(node)
        self.state.transform.scaling = node.scale
        return node

    def on_m00(self, node: M00) -> M00:
        """Handle `M00` node."""
        raise ProgramStop(node)

    def on_m02(self, node: M02) -> M02:
        """Handle `M02` node."""
        raise ProgramStop(node)

    def on_coordinate_x(self, node: CoordinateX) -> CoordinateX:
        """Handle `Coordinate` node."""
        super().on_coordinate_x(node)
        if self.state.coordinate_format is None:
            raise CoordinateFormatNotSetError(node)

        self.state.coordinate_x = self.state.coordinate_format.unpack_x(node.value)
        return node

    def on_coordinate_y(self, node: CoordinateY) -> CoordinateY:
        """Handle `Coordinate` node."""
        super().on_coordinate_y(node)
        if self.state.coordinate_format is None:
            raise CoordinateFormatNotSetError(node)

        self.state.coordinate_y = self.state.coordinate_format.unpack_y(node.value)
        return node

    def on_coordinate_i(self, node: CoordinateI) -> CoordinateI:
        """Handle `Coordinate` node."""
        super().on_coordinate_i(node)
        if self.state.coordinate_format is None:
            raise CoordinateFormatNotSetError(node)

        self.state.coordinate_i = self.state.coordinate_format.unpack_x(node.value)
        return node

    def on_coordinate_j(self, node: CoordinateJ) -> CoordinateJ:
        """Handle `Coordinate` node."""
        super().on_coordinate_j(node)
        if self.state.coordinate_format is None:
            raise CoordinateFormatNotSetError(node)

        self.state.coordinate_j = self.state.coordinate_format.unpack_y(node.value)
        return node

    def on_as(self, node: AS) -> AS:
        """Handle `AS` node."""
        super().on_as(node)
        self.state.image_attributes.axis_correspondence = node.correspondence
        return node

    def on_fs(self, node: FS) -> FS:
        """Handle `FS` node."""
        super().on_fs(node)
        self.state.coordinate_format = CoordinateFormat(
            zeros=node.zeros,
            coordinate_mode=node.coordinate_mode,
            x_integral=node.x_integral,
            x_decimal=node.x_decimal,
            y_integral=node.y_integral,
            y_decimal=node.y_decimal,
        )
        return node

    def on_in(self, node: IN) -> IN:
        """Handle `IN` node."""
        super().on_in(node)
        self.state.image_attributes.image_name = node.name
        return node

    def on_ip(self, node: IP) -> IP:
        """Handle `IP` node."""
        super().on_ip(node)
        self.state.image_attributes.polarity = node.polarity
        return node

    def on_ir(self, node: IR) -> IR:
        """Handle `IR` node."""
        super().on_ir(node)
        self.state.image_attributes.rotation = node.rotation_degrees
        return node

    def on_mi(self, node: MI) -> MI:
        """Handle `MI` node."""
        super().on_mi(node)
        self.state.image_attributes.a_axis_mirroring = node.a_mirroring
        self.state.image_attributes.b_axis_mirroring = node.b_mirroring
        return node

    def on_mo(self, node: MO) -> MO:
        """Handle `MO` node."""
        super().on_mo(node)
        self.state.unit_mode = node.mode
        return node

    def on_of(self, node: OF) -> OF:
        """Handle `OF` node."""
        super().on_of(node)
        self.state.image_attributes.a_axis_offset = node.a_offset
        self.state.image_attributes.b_axis_offset = node.b_offset
        return node

    def on_sf(self, node: SF) -> SF:
        """Handle `SF` node."""
        super().on_sf(node)
        self.state.image_attributes.a_axis_scale = node.a_scale
        self.state.image_attributes.b_axis_scale = node.b_scale
        return node

    def on_file(self, node: File) -> File:
        """Handle `File` node."""
        with suppress(ProgramStop):
            super().on_file(node)
        return node

    def on_exception(self, node: Node, exception: Exception) -> bool:  # noqa: ARG002
        """Handle exception."""
        if isinstance(exception, ProgramStop):
            return bool(self._ignore_program_stop)

        return True
