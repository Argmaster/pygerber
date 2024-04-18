"""Block Aperture (AB) logic."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class BlockApertureBegin(CommandToken):
    """## 4.11 Block Aperture (AB).

    ### 4.11.1 Overview of block apertures

    The AB command creates a block aperture. The command stream between the opening and
    closing AB command defines a block aperture which is stored in the aperture dictionary. Thus
    the AB commands add an aperture to the dictionary directly, without needing an AD command.
    The LM, LR, LS and LP commands affect the flashes of block apertures as any other aperture:
    when a block aperture is flashed, it is first transformed according to the transformation
    parameters in the graphics state and then added to the object stream.

    The origin of the block aperture is the (0,0) point of the file.

    A block aperture is not a single graphical object but a set of objects. While a standard or macro
    aperture always adds a single graphical object to the stream, a block aperture can add any
    number of objects, each with their own polarity. Standard and macro apertures always have a
    single polarity while block apertures can contain both dark and clear objects.

    If the polarity is dark (LPD) when the block is flashed then the block aperture is inserted as is. If
    the polarity is clear (LPC) then the polarity of all objects in the block is toggled (clear becomes
    dark, and dark becomes clear). This toggle propagates through all nesting levels. In the
    following example the polarity of objects in the flash of block D12 will be toggled.

    ```gerber
    %ABD12*%
    …
    %AB*%
    …
    D12*
    %LPC*%
    X-2500000Y-1000000D03*
    ```

    A D03 of a block aperture updates the current point but otherwise leaves the graphics state
    unmodified, as with any other aperture.

    ---

    See section 4.11 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=111)

    """  # noqa: E501

    def __init__(self, string: str, location: int, identifier: ApertureID) -> None:
        super().__init__(string, location)
        self.identifier = identifier

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        return cls(string, location, ApertureID(tokens["aperture_identifier"]))

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.identifier)
        with handle:
            # Must be included to initialize drawing target.
            pass
        frozen_handle = handle.get_public_handle()

        new_aperture_dict = {**state.apertures}
        new_aperture_dict[self.identifier] = frozen_handle

        return (
            state.model_copy(
                update={
                    "apertures": new_aperture_dict,
                },
            ),
            (),
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().begin_block_aperture.pre_parser_visit_token(self, context)
        context.get_hooks().begin_block_aperture.on_parser_visit_token(self, context)
        context.get_hooks().begin_block_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}AB{self.identifier.get_gerber_code()}"


class BlockApertureEnd(CommandToken):
    """## 4.11 Block Aperture (AB).

    ### 4.11.1 Overview of block apertures

    The AB command creates a block aperture. The command stream between the opening and
    closing AB command defines a block aperture which is stored in the aperture dictionary. Thus
    the AB commands add an aperture to the dictionary directly, without needing an AD command.
    The LM, LR, LS and LP commands affect the flashes of block apertures as any other aperture:
    when a block aperture is flashed, it is first transformed according to the transformation
    parameters in the graphics state and then added to the object stream.

    The origin of the block aperture is the (0,0) point of the file.

    A block aperture is not a single graphical object but a set of objects. While a standard or macro
    aperture always adds a single graphical object to the stream, a block aperture can add any
    number of objects, each with their own polarity. Standard and macro apertures always have a
    single polarity while block apertures can contain both dark and clear objects.

    If the polarity is dark (LPD) when the block is flashed then the block aperture is inserted as is. If
    the polarity is clear (LPC) then the polarity of all objects in the block is toggled (clear becomes
    dark, and dark becomes clear). This toggle propagates through all nesting levels. In the
    following example the polarity of objects in the flash of block D12 will be toggled.

    ```gerber
    %ABD12*%
    …
    %AB*%
    …
    D12*
    %LPC*%
    X-2500000Y-1000000D03*
    ```

    A D03 of a block aperture updates the current point but otherwise leaves the graphics state
    unmodified, as with any other aperture.

    ---

    See section 4.11 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=111)

    """  # noqa: E501

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().end_block_aperture.pre_parser_visit_token(self, context)
        context.get_hooks().end_block_aperture.on_parser_visit_token(self, context)
        context.get_hooks().end_block_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}AB"
