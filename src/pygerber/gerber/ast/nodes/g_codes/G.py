"""`pygerber.nodes.g_codes.G01` module contains definition of `G01` class."""

from __future__ import annotations

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node


class G(Node):
    """Base class for all Gxx nodes."""

    is_standalone: bool = Field(default=True)
    """Flag indicating if the node is standalone, ie. it should include * at the end.

    This is necessary as some legacy Gerber files use redundant G codes to prefix
    pretty much every D01/D02/D03 command. To make it possible to keep the original
    layout of the file, we need to know if the G code was directly followed by a D code.

    Example:

    ```gerber
    G70D02*
    G54D16*
    G01X5440Y5650D03*
    G01X5440Y6900D03*
    G01X6800Y2200D03*
    G01X5550Y2200D03*
    G01X17720Y6860D03*
    G01X17720Y5610D03*
    ```
    """
