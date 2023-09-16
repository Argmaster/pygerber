"""Wrapper for G91 token."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class SetIncrementalNotation(Token):
    """Wrapper for G91 token.

    Set the `Coordinate format` to `Incremental notation`.

    This historic code performs a function handled by the FS command. See 4.1. Very
    rarely used nowadays. Deprecated in 2012.

    See section 8.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    @classmethod
    def from_tokens(cls, **_tokens: Any) -> Self:
        """Initialize token object."""
        return cls()

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        warn_deprecated_code("G91", "8.1")
        if state.coordinate_parser is not None:
            logging.warning(
                "Overriding coordinate format is illegal. "
                "(See section 4.2.2 of The Gerber Layer Format Specification "
                "Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html)",
            )

        msg = "Incremental notation not supported."
        raise NotImplementedError(msg)

    def __str__(self) -> str:
        return "G91*"
