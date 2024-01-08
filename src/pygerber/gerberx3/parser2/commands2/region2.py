"""Parser level abstraction of draw region operation for Gerber AST parser,
version 2.
"""
from __future__ import annotations

from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2


class Region2(BufferCommand2):
    """Parser level abstraction of draw region operation for Gerber AST parser,
    version 2.
    """

    command_buffer: ReadonlyCommandBuffer2

    def command_to_json(self) -> str:
        """Dump draw operation."""
        return f"""{{ "cls": "{self.__module__}.{self.__class__.__qualname__}", "dict": {{
        "polarity": "{self.polarity.value}",
        "attributes": {self.attributes.model_dump_json()},
        "command_buffer": {
            self.command_buffer.debug_buffer_to_json(8)}
    }}
}}"""  # noqa: E501
