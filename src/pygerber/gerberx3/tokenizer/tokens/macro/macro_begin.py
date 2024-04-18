"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class MacroBegin(Token):
    """## 4.5 Aperture Macro (AM).

    The AM command creates a macro aperture `template` and adds it to the aperture `template`
    dictionary (see 2.2). A `template` is a parametrized shape. The AD command instantiates a
    `template` into an aperture by supplying values to the template `parameters`.

    Templates of any shape or parametrization can be created. Multiple simple shapes called
    `primitives` can be combined in a single `template`. An aperture macro can contain `variables`
    whose actual values are defined by:

    - Values provided by the AD command
    - `Arithmetic expressions` with other `variables`

    The template is created by positioning `primitives` in a coordinate space. The origin of that
    coordinate space will be the origin of all apertures created with the state.

    A `template` must be defined before the first AD that refers to it. The AM command can be used
    multiple times in a file.

    `Attributes` are not attached to templates. They are attached to the aperture at the time of its
    creation with the AD command.

    An AM command contains the following words:

    - The AM declaration with the macro name
    - `Primitives` with their comma-separated `parameters`
    - `Macro variables`, defined by an `arithmetic expression`

    Coordinates and sizes are expressed in the unit set by the MO command.

    A parameter can be either:

    - A `decimal` number
    - A `macro variable`
    - An `arithmetic expression`

    A `macro variable` name must be a "$" character followed by an integer >0, for example `$12`.
    (This is a subset of names allowed in 3.4.3.)

    ---

    ## Example

    The following AM command defines an aperture macro named "Triangle_30".

    ```gerber
    %AMTriangle_30*
    4,1,3,
    1,-1,
    1,1,
    2,1,
    1,-1,
    30*
    %
    ```

    ---

    See section 4.5 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=56)

    """  # noqa: E501

    def __init__(self, string: str, location: int, name: str) -> None:
        super().__init__(string, location)
        self.name = name

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        content: str = str(tokens["macro_name"])
        return cls(string=string, location=location, name=content)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_begin.pre_parser_visit_token(self, context)
        context.get_hooks().macro_begin.on_parser_visit_token(self, context)
        context.get_hooks().macro_begin.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"AM{self.name}"

    def get_gerber_code_one_line_pretty_display(self) -> str:
        """Get gerber code represented by this token."""
        return f"%{self.get_gerber_code()}*"
