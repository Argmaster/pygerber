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
from pygerber.gerberx3.state_enums import AxisCorrespondence
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class AxisSelect(ExtendedCommandToken):
    """## 8.1.2 Axis Select (AS).

    The AS command is deprecated since revision I1 from December 2012.

    The historic AS command sets the correspondence between the X, Y data axes and the
    A, B output device axes. It does not affect the image in computer to computer data
    exchange. It only has an effect how the image is positioned on an output device.

    The order of execution is always MI, SF, OF, IR and AS, independent of their order
    of appearance in the file.

    The AS command can only be used once, at the beginning of the file.

    ### 8.1.2.1 AS Command.

    The syntax for the AS command is:

    ```ebnf
    AS = '%' (AS' ('AXBY'|'AYBX')) '*%';
    ```

    - `AS` - AS for Axis Select
    - `AXBY` - Assign output device axis A to data axis X, output device axis B to data axis Y. This is the default.
    - `AYBX` - Assign output device axis A to data axis Y, output device axis B to data axis X.

    ---

    ## Example

    Assign output device axis A to data axis X and output device axis B
    to data axis Y

    ```gerber
    %ASAXBY*%
    ```

    Assign output device axis A to data axis Y and output device axis B
    to data axis X

    ```gerber
    %ASAYBX*%
    ```

    ---

    See section 8.1.2 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=175)

    """  # noqa: E501

    def __init__(
        self,
        string: str,
        location: int,
        correspondence: AxisCorrespondence,
    ) -> None:
        super().__init__(string, location)
        self.correspondence = correspondence

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        correspondence = tokens["correspondence"]
        if not isinstance(correspondence, str):
            raise TypeError(correspondence)
        return cls(
            string=string,
            location=location,
            correspondence=AxisCorrespondence(correspondence),
        )

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        warn_deprecated_code("AS", "8.1")
        return super().update_drawing_state(state, _backend)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().axis_select.pre_parser_visit_token(self, context)
        context.get_hooks().axis_select.on_parser_visit_token(self, context)
        context.get_hooks().axis_select.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"IN{self.correspondence}"
