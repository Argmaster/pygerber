"""### Load Name (LN).

Note: The LN command was deprecated in revision I4 from October 2013.

The historic `LN` command doesn't influence the image in any manner and can safely be
overlooked.

Function of the `LN` command:
- `LN` is designed to allocate a name to the following section of the file.
- It was originally conceptualized to serve as a human-readable comment.
- For creating human-readable comments, it's advisable to utilize the standard `G04`
    command.
- The `LN` command has the flexibility to be executed multiple times within a file.

SPEC: `2023.03` SECTION: `8.1.6`
"""


from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class LoadName(ExtendedCommandToken):
    """Comment token.

    ### Load Name (LN)

    Note: The LN command was deprecated in revision I4 from October 2013.

    The historic `LN` command doesn't influence the image in any manner and can safely
    be overlooked.

    Function of the `LN` command:
    - `LN` is designed to allocate a name to the following section of the file.
    - It was originally conceptualized to serve as a human-readable comment.
    - For creating human-readable comments, it's advisable to utilize the standard `G04`
        command.
    - The `LN` command has the flexibility to be executed multiple times within a file.

    See section 8.1.6 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(self, string: str, location: int, content: str) -> None:
        super().__init__(string, location)
        self.content = content

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        content: str = str(tokens["string"])
        return cls(string=string, location=location, content=content)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        warn_deprecated_code("LN", "8.1")
        return super().update_drawing_state(state, _backend)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"LN{self.content}"
