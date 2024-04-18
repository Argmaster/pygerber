"""Wrapper for image polarity token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.state_enums import ImagePolarityEnum
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class ImagePolarity(ExtendedCommandToken):
    """Wrapper for image polarity token.

    The IP command is deprecated.

    IP sets positive or negative polarity for the entire image. It can only be used
    once, at the beginning of the file.

    See section 8.1.4 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        image_polarity: ImagePolarityEnum,
    ) -> None:
        super().__init__(string, location)
        self.image_polarity = image_polarity

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        image_polarity = ImagePolarityEnum(tokens["image_polarity"])
        return cls(
            string=string,
            location=location,
            image_polarity=image_polarity,
        )

    def update_drawing_state(
        self,
        state: State,
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set drawing polarity."""
        warn_deprecated_code("IP", "8.1.4")
        return (
            state.model_copy(
                update={
                    "is_output_image_negation_required": (
                        self.image_polarity == ImagePolarityEnum.NEGATIVE
                    ),
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().image_polarity.pre_parser_visit_token(self, context)
        context.get_hooks().image_polarity.on_parser_visit_token(self, context)
        context.get_hooks().image_polarity.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return f"IP{self.image_polarity.get_gerber_code(indent, endline)}"
