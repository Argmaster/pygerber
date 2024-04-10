"""Module contains base class Rendering backend for Parser2 based Gerber data
structures.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, Generator, Optional

from pygerber.gerberx3.parser2.apertures2.circle2 import Circle2, NoCircle2
from pygerber.gerberx3.parser2.apertures2.macro2 import Macro2
from pygerber.gerberx3.parser2.apertures2.obround2 import Obround2
from pygerber.gerberx3.parser2.apertures2.polygon2 import Polygon2
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2
from pygerber.gerberx3.parser2.command_buffer2 import (
    ReadonlyCommandBuffer2,
)
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2, CCArc2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.commands2.region2 import Region2

if TYPE_CHECKING:
    from io import BytesIO


class Renderer2:
    """Rendering backend base class for Parser2 based Gerber data structures."""

    def __init__(self, hooks: Renderer2HooksABC) -> None:
        self.hooks = hooks

    def render(self, command_buffer: ReadonlyCommandBuffer2) -> ImageRef:
        """Render Gerber structures."""
        for _ in self.render_iter(command_buffer):
            pass

        return self.get_image_ref()

    def get_image_ref(self) -> ImageRef:
        """Get reference to render image."""
        return self.hooks.get_image_ref()

    def render_iter(
        self,
        command_buffer: ReadonlyCommandBuffer2,
    ) -> Generator[Command2, None, None]:
        """Iterate over commands in buffer and render image for each command."""
        self.hooks.init(self, command_buffer)
        for command in command_buffer:
            yield from command.render_iter(self)
        self.hooks.finalize()


class Renderer2HooksABC:
    """Hooks for implementing rendering of Gerber structures to a target format."""

    def init(self, renderer: Renderer2, command_buffer: ReadonlyCommandBuffer2) -> None:
        """Initialize rendering."""
        self.renderer = renderer
        self.command_buffer = command_buffer

    def render_line(self, command: Line2) -> None:
        """Render line to target image."""

    def render_arc(self, command: Arc2) -> None:
        """Render arc to target image."""

    def render_cc_arc(self, command: CCArc2) -> None:
        """Render arc to target image."""

    def render_flash_circle(self, command: Flash2, aperture: Circle2) -> None:
        """Render flash circle to target image."""

    def render_flash_no_circle(self, command: Flash2, aperture: NoCircle2) -> None:
        """Render flash no circle aperture to target image."""

    def render_flash_rectangle(self, command: Flash2, aperture: Rectangle2) -> None:
        """Render flash rectangle to target image."""

    def render_flash_obround(self, command: Flash2, aperture: Obround2) -> None:
        """Render flash obround to target image."""

    def render_flash_polygon(self, command: Flash2, aperture: Polygon2) -> None:
        """Render flash polygon to target image."""

    def render_flash_macro(self, command: Flash2, aperture: Macro2) -> None:
        """Render flash macro aperture to target image."""

    def render_buffer(self, command: BufferCommand2) -> Generator[Command2, None, None]:
        """Render buffer command, performing no writes."""
        for cmd in command:
            cmd.render(self.renderer)
            yield cmd

    def render_region(self, command: Region2) -> None:
        """Render region to target image."""

    def get_image_ref(self) -> ImageRef:
        """Get reference to render image."""
        raise NotImplementedError

    def finalize(self) -> None:
        """Finalize rendering."""


class ImageRef:
    """Generic container for reference to rendered image."""

    def save_to(
        self,
        dest: BytesIO | Path | str,
        options: Optional[FormatOptions] = None,
    ) -> None:
        """Save rendered image."""
        if isinstance(dest, str):
            dest = Path(dest)
        if isinstance(dest, Path):
            with dest.open("wb") as output:
                return self._save_to_io(output, options)
        else:
            return self._save_to_io(dest, options)

    def _save_to_io(
        self,
        output: BinaryIO,
        options: Optional[FormatOptions] = None,
    ) -> None:
        """Save rendered image to bytes stream buffer."""
        raise NotImplementedError


class FormatOptions:
    """Base class for representing of possible format options."""
