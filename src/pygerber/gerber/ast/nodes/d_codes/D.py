"""`pygerber.nodes.d_codes.DNN` module contains definition of `DNN` class."""

from __future__ import annotations

from pydantic import Field

from pygerber.gerber.ast.nodes.base import Node


class D(Node):
    """Base class for all Dxx commands."""

    is_standalone: bool = Field(default=True)
    """Flag indicating if the node is standalone, ie. it is not prefixed with
    G code with no asterisk.

    This is necessary as some legacy Gerber files use redundant G codes to prefix
    pretty much every D01/D02/D03 command. To make it possible to keep the original
    layout of the file, we need to know if the D code was directly prefixed by
    such redundant G code.

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
