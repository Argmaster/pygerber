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

from decimal import Decimal
from typing import TYPE_CHECKING, Iterable, Optional, Tuple

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

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class ImageOffset(ExtendedCommandToken):
    """### Image Offset (OF).

    The OF command is deprecated since revision I1 from December 2012.

    OF moves the final image up to plus or minus 99999.99999 units from the imaging
    device (0, 0) point. The image can be moved along the imaging device A or B axis,
    or both. The offset values used by OF command are absolute. If the A or B part is
    missing, the corresponding offset is 0. The offset values are expressed in units
    specified by MO command.  This command affects the entire image. It can only be
    used once, at the beginning of the file. The order of execution is always MI, SF,
    OF, IR and AS, independent of their order of appearance in the file.

    See section 8.1.8 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        a: Optional[Decimal],
        b: Optional[Decimal],
    ) -> None:
        super().__init__(string, location)
        self.a = a
        self.b = b

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        a = Decimal(str(tmp)) if (tmp := tokens.get("a")) is not None else None
        b = Decimal(str(tmp)) if (tmp := tokens.get("b")) is not None else None
        return cls(string=string, location=location, a=a, b=b)

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        warn_deprecated_code("IN", "8.1")
        return super().update_drawing_state(state, _backend)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().image_offset.pre_parser_visit_token(self, context)
        context.get_hooks().image_offset.on_parser_visit_token(self, context)
        context.get_hooks().image_offset.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        a = f"A{self.a}" if self.a is not None else ""
        b = f"B{self.b}" if self.b is not None else ""
        return f"OF{a}{b}"
