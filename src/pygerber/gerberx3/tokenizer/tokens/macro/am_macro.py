"""Container token for macro definition."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Sequence, Tuple

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.bases.group import TokenGroup
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_begin import MacroBegin
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class MacroDefinition(TokenGroup):
    """Container token for macro definition."""

    tokens: Sequence[Token | Expression]

    def __init__(
        self,
        string: str,
        location: int,
        tokens: Sequence[Token | Expression],
    ) -> None:
        super().__init__(string, location, tokens)

    @property
    def macro_name(self) -> str:
        """Name of macro item."""
        macro_begin = self.tokens[0]
        if not isinstance(macro_begin, MacroBegin):
            raise TypeError(macro_begin)
        return macro_begin.name

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

        macro_tokens = [macro_begin, *macro_body_tokens]

        return cls(
            string=string,
            location=location,
            tokens=macro_tokens,
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
            if isinstance(expression, Expression):
                expression.evaluate(context, state, handle)
