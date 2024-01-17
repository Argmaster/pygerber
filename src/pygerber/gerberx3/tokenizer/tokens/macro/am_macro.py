"""Container token for macro definition."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Iterator, List, Tuple

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.bases.group import TokenGroup
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.macro.macro_begin import MacroBegin
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.statements.statement import (
    MacroStatementToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class MacroDefinition(TokenGroup):
    """## 4.5 Aperture Macro (AM).

    The AM command creates a macro aperture template and adds it to the aperture template
    dictionary (see 2.2). A template is a parametrized shape. The AD command instantiates a
    template into an aperture by supplying values to the template parameters.

    Templates of any shape or parametrization can be created. Multiple simple shapes called
    primitives can be combined in a single template. An aperture macro can contain variables
    whose actual values are defined by:

    - Values provided by the AD command,
    - Arithmetic expressions with other variables.

    The template is created by positioning primitives in a coordinate space. The origin of that
    coordinate space will be the origin of all apertures created with the state.

    A template must be defined before the first AD that refers to it. The AM command can be used
    multiple times in a file.

    Attributes are not attached to templates. They are attached to the aperture at the time of its
    creation with the AD command.

    An AM command contains the following words:

    - The AM declaration with the macro name
    - Primitives with their comma-separated parameters
    - Macro variables, defined by an arithmetic expression

    ---

    ### Syntax

    ```ebnf
    AM = '%' ('AM' macro_name macro_body) '%';
    macro_name = name '*';
    macro_body = {in_macro_block}+;
    in_macro_block =
    |primitive
    |variable_definition
    ;
    variable_definition = (macro_variable '=' expression) '*';
    macro_variable = '$' positive_integer;
    primitive = primitive_code {',' par}*
    par = ',' (expression);
    ```

    - `AM` - AM for Aperture Macro
    - `<Macro name>` - Name of the aperture macro. The name must be unique, it
        cannot be reused for another macro. See [3.4.5](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=36)
        for the syntax rules.
    - `<Macro body>` - The macro body contains the primitives generating the image
        and the calculation of their parameters.
    - `<Variable definition>` - `$n=<Arithmetic expression>`. An arithmetic expression may
        use arithmetic operators (described later), constants and
        variables $m defined previously.
    - `<Primitive>` - A primitive is a basic shape to create the macro. It includes
        primitive code identifying the primitive and primitive-specific
        parameters (e.g. center of a circle). See [4.5.1](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=58).
        The primitives are positioned in a coordinates system whose origin is the
        origin of the resulting apertures.
    - `<Primitive code>` - A code specifying the primitive (e.g. polygon).
    - `<Parameter>` - Parameter can be a decimal number (e.g. `0.050`), a variable
        (e.g. `$1`) or an arithmetic expression based on numbers and
        variables. The actual value is calculated as explained in
        [4.5.4.3](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=71).

    Coordinates and sizes are expressed in the unit set by the MO command.

    A parameter can be either:

    - A decimal number
    - A macro variable
    - An arithmetic expression

    A macro variable name must be a `$` character followed by an integer >0, for example `$12`.
    (This is a subset of names allowed in [3.4.3](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=35).)

    **Note:** New lines can be added between words of a single command to enhance
    readability. They do not affect the macro definition.

    ### Example

    The following AM command defines an aperture macro named 'Triangle_30'.

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

    begin: MacroBegin
    tokens: List[Token]

    def __init__(
        self,
        string: str,
        location: int,
        macro_begin: MacroBegin,
        tokens: List[Token],
    ) -> None:
        super().__init__(string, location, tokens)
        self.macro_begin = macro_begin

    @property
    def macro_name(self) -> str:
        """Name of macro item."""
        return self.macro_begin.name

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        macro_begin = tokens["macro_begin"]
        if not isinstance(macro_begin, MacroBegin):
            raise TypeError(macro_begin)

        macro_body_raw = tokens["macro_body"]
        macro_body_tokens: list[Token] = []

        for e in macro_body_raw:
            token = e[0]
            if not isinstance(token, Token):
                raise TypeError(token)
            macro_body_tokens.append(token)

        return cls(
            string=string,
            location=location,
            macro_begin=macro_begin,
            tokens=macro_body_tokens,
        )

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Exit drawing process."""
        new_macros_dict = {**state.macros}
        new_macros_dict[self.macro_name] = self

        return (
            state.model_copy(
                update={
                    "macros": new_macros_dict,
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_definition.pre_parser_visit_token(self, context)
        context.get_hooks().macro_definition.on_parser_visit_token(self, context)
        context.get_hooks().macro_definition.post_parser_visit_token(self, context)

    def __iter__(self) -> Iterator[Token]:
        yield self.macro_begin
        for token in self.tokens:
            yield from token
        yield self

    def evaluate(
        self,
        state: State,
        handle: PrivateApertureHandle,
        parameters: dict[str, Offset],
    ) -> None:
        """Evaluate macro into series of DrawCommands."""
        context = MacroContext()
        context.variables.update(parameters)

        for expression in self.tokens:
            if isinstance(expression, MacroStatementToken):
                expression.evaluate(context, state, handle)
