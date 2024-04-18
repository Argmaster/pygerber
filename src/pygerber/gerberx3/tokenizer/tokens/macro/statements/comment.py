"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.macro.statements.statement import (
    MacroStatementToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class MacroComment(MacroStatementToken):
    """## 4.5.1.2 Comment, Code 0.

    The comment primitive has no effect on the image but adds human-readable comments
    in an AM command. The comment primitive starts with the '0' code followed by a space
    and then a single-line text string. The text string follows the syntax for strings
    in section 3.4.3.

    ---

    ## Example

    ```gerber
    %AMBox*
    0 Rectangle with rounded corners, with rotation*
    0 The origin of the aperture is its center*
    0 $1 X-size*
    0 $2 Y-size*
    0 $3 Rounding radius*
    0 $4 Rotation angle, in degrees counterclockwise*
    0 Add two overlapping rectangle primitives as box body*
    21,1,$1, $2-$3-$3,0,0,$4
    21,1,$1-$3-$3,$2,0,0,$4*
    0 Add four circle primitives for the rounded corners*
    $5-$1/2*
    $6-$2/2*
    $7=2x$3*
    1,1, $7, $5-$3, $6-$3, $4*
    1,1, $7-$5+$3,$6-$3, $4*
    1,1, $7-$5+$3,-$6+$3, $4*
    1,1, $7, $5-$3,-$6+$3, $4*%
    ```

    ---

    See section 4.5.1.2 of [The Gerber Layer Format Specification Revision 2023.03](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-03_en.pdf#page=59)
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

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}0 {self.content}"
