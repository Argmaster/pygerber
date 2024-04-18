"""Coordinate format token."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser.errors import (
    IncrementalCoordinatesNotSupportedError,
    InvalidCoordinateLengthError,
    UnsupportedCoordinateTypeError,
    ZeroOmissionNotSupportedError,
)
from pygerber.gerberx3.tokenizer.helpers.gerber_code_enum import GerberCodeEnum
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)
from pygerber.gerberx3.tokenizer.tokens.bases.gerber_code import GerberCode
from pygerber.gerberx3.tokenizer.tokens.coordinate import (
    Coordinate,
    CoordinateSign,
    CoordinateType,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


RECOMMENDED_MINIMAL_DECIMAL_PLACES = 5


class CoordinateFormat(ExtendedCommandToken):
    """Description of coordinate format token.

    See:
    -   section 4.1.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    -   section 4.2.2 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        zeros_mode: TrailingZerosMode,
        coordinate_mode: CoordinateMode,
        x_format: AxisFormat,
        y_format: AxisFormat,
    ) -> None:
        super().__init__(string, location)
        self.zeros_mode = zeros_mode
        self.coordinate_mode = coordinate_mode
        self.x_format = x_format
        self.y_format = y_format

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        zeros_mode = TrailingZerosMode(tokens["zeros_mode"])
        coordinate_mode = CoordinateMode(tokens["coordinate_mode"])
        x_format = AxisFormat(
            integer=int(str(tokens["x_format"][0])),
            decimal=int(str(tokens["x_format"][1])),
        )
        y_format = AxisFormat(
            integer=int(str(tokens["y_format"][0])),
            decimal=int(str(tokens["y_format"][1])),
        )
        return cls(
            string=string,
            location=location,
            zeros_mode=zeros_mode,
            coordinate_mode=coordinate_mode,
            x_format=x_format,
            y_format=y_format,
        )

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set coordinate parser."""
        if state.coordinate_parser is not None:
            logging.warning(
                "Overriding coordinate format is illegal."
                "(See 4.2.2 in Gerber Layer Format Specification)",
            )
        return (
            state.model_copy(
                update={
                    "coordinate_parser": CoordinateParser.new(
                        x_format=self.x_format,
                        y_format=self.y_format,
                    ),
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().coordinate_format.pre_parser_visit_token(self, context)
        context.get_hooks().coordinate_format.on_parser_visit_token(self, context)
        context.get_hooks().coordinate_format.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return (
            f"FS"
            f"{self.zeros_mode.get_gerber_code(indent, endline)}"
            f"{self.coordinate_mode.get_gerber_code(indent, endline)}"
            f"X{self.x_format.get_gerber_code(indent, endline)}"
            f"Y{self.y_format.get_gerber_code(indent, endline)}"
        )


class TrailingZerosMode(GerberCodeEnum):
    """Coordinate format mode.

    GerberX3 supports only one, L, the other is required for backwards compatibility.
    """

    OmitLeading = "L"
    OmitTrailing = "T"


class CoordinateMode(GerberCodeEnum):
    """Coordinate format mode.

    GerberX3 supports only one, A, the other required for backwards compatibility.
    """

    Absolute = "A"
    Incremental = "I"


class AxisFormat(FrozenGeneralModel, GerberCode):
    """Wrapper for single axis format."""

    integer: int
    decimal: int

    @property
    def total_length(self) -> int:
        """Total format length."""
        return self.integer + self.decimal

    def __str__(self) -> str:
        return f"{self.integer}{self.decimal}"

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}{self.integer}{self.decimal}"


class CoordinateParser(FrozenGeneralModel):
    """Coordinate Parser class."""

    x_format: AxisFormat
    y_format: AxisFormat

    @classmethod
    def new(
        cls,
        x_format: AxisFormat,
        y_format: AxisFormat,
        coordinate_mode: CoordinateMode = CoordinateMode.Absolute,
        zeros_mode: TrailingZerosMode = TrailingZerosMode.OmitLeading,
    ) -> Self:
        """Update coordinate parser format configuration."""
        if coordinate_mode != CoordinateMode.Absolute:
            raise IncrementalCoordinatesNotSupportedError

        if zeros_mode != TrailingZerosMode.OmitLeading:
            raise ZeroOmissionNotSupportedError

        for axis, axis_format in (("X", x_format), ("Y", y_format)):
            if axis_format.decimal < RECOMMENDED_MINIMAL_DECIMAL_PLACES:
                logging.warning(
                    "It is recommended to use at least 5 decimal places for coordinate "
                    "data when using metric units and 6 decimal places for imperial "
                    "units. (Detected for %s)"
                    "(See 4.2.2 in Gerber Layer Format Specification)",
                    axis,
                )

        return cls(x_format=x_format, y_format=y_format)

    def parse(self, coordinate: Coordinate) -> Decimal:
        """Parse raw coordinate data."""
        if coordinate.coordinate_type in (CoordinateType.X, CoordinateType.I):
            return self._parse(self.x_format, coordinate.offset, coordinate.sign)

        if coordinate.coordinate_type in (CoordinateType.Y, CoordinateType.J):
            return self._parse(self.y_format, coordinate.offset, coordinate.sign)

        raise UnsupportedCoordinateTypeError(coordinate.coordinate_type)

    def _parse(
        self,
        axis_format: AxisFormat,
        offset: str,
        sign: CoordinateSign,
    ) -> Decimal:
        total_length = axis_format.total_length

        if len(offset) > total_length:
            msg = f"Got {offset!r} with length {len(offset)} expected {total_length}."
            raise InvalidCoordinateLengthError(msg)

        offset = offset.rjust(axis_format.total_length, "0")
        integer, decimal = offset[: axis_format.integer], offset[axis_format.integer :]

        return Decimal(f"{sign.value}{integer}.{decimal}")
