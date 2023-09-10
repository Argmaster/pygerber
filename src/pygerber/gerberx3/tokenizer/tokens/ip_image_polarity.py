"""Wrapper for image polarity token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.state_enums import ImagePolarityEnum
from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.warnings import warn_deprecated_code

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class ImagePolarity(Token):
    """Wrapper for image polarity token.

    The IP command is deprecated.

    IP sets positive or negative polarity for the entire image. It can only be used
    once, at the beginning of the file.

    See section 8.1.4 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    image_polarity: ImagePolarityEnum

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        image_polarity = ImagePolarityEnum(tokens["image_polarity"])
        return cls(image_polarity=image_polarity)

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

    def __str__(self) -> str:
        return f"%IP{self.image_polarity}*%"
