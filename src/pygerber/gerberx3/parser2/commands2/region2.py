"""Parser level abstraction of draw region operation for Gerber AST parser,
version 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from pydantic import Field

from pygerber.gerberx3.parser2.attributes2 import ApertureAttributes, ObjectAttributes
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2
from pygerber.gerberx3.parser2.commands2.command2 import Command2

if TYPE_CHECKING:
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Region2(BufferCommand2):
    """Parser level abstraction of draw region operation for Gerber AST parser,
    version 2.
    """

    aperture_attributes: ApertureAttributes = Field(default_factory=ApertureAttributes)
    object_attributes: ObjectAttributes = Field(default_factory=ObjectAttributes)
    command_buffer: ReadonlyCommandBuffer2

    def command_to_json(self) -> str:
        """Dump draw operation."""
        return f"""{{ "cls": "{self.__module__}.{self.__class__.__qualname__}", "dict": {{
        "polarity": "{self.transform.polarity.value}",
        "aperture_attributes": {self.aperture_attributes.model_dump_json()},
        "command_buffer": {self.command_buffer.model_dump_json()},
        "command_buffer": {
            self.command_buffer.debug_buffer_to_json(8)}
    }}
}}"""  # noqa: E501

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        renderer.hooks.render_region(self)

    def render_iter(self, renderer: Renderer2) -> Generator[Command2, None, None]:
        """Render draw operation."""
        renderer.hooks.render_region(self)
        yield self
