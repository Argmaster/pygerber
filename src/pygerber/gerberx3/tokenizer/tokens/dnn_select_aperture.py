"""Wrapper for aperture select token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pydantic_core import CoreSchema, core_schema

from pygerber.gerberx3.parser.errors import ApertureNotDefinedError
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class DNNSelectAperture(Token):
    """Wrapper for aperture select token.

    Sets the current aperture to D code NN (NN ≥ 10).
    """

    aperture_id: ApertureID

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_id: ApertureID = tokens["aperture_identifier"]
        return cls(aperture_id=aperture_id)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set current aperture."""
        if self.aperture_id not in state.apertures:
            raise ApertureNotDefinedError(self.aperture_id)
        return (
            state.model_copy(
                update={
                    "current_aperture": state.apertures[self.aperture_id],
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"{self.aperture_id}*"


class ApertureID(str):
    """Aperture ID wrapper."""

    __slots__ = ()

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Generate the pydantic-core schema."""
        return core_schema.no_info_after_validator_function(cls, handler(str))
