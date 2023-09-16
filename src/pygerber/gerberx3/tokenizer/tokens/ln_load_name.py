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

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from typing_extensions import Self


class LoadName(Token):
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

    content: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        content: str = tokens["string"]
        return cls(content=content)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        warn_deprecated_code("LN", "8.1")
        return super().update_drawing_state(state, _backend)

    def __str__(self) -> str:
        return f"%LN {self.content}*%"
