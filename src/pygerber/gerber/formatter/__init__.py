"""The `formatter` package contains implementation of Gerber X3 formatter."""

from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, Optional, TextIO

from pygerber.gerber.formatter.enums import (
    EmptyLineBeforePolaritySwitch,
    ExplicitParenthesis,
    FloatTrimTrailingZeros,
    KeepNonStandaloneCodes,
    MacroEndInNewLine,
    MacroSplitMode,
    RemoveG54,
    RemoveG55,
    StripWhitespace,
)
from pygerber.gerber.formatter.formatter import Formatter
from pygerber.gerber.formatter.options import Options
from pygerber.gerber.formatter.presets import balanced, extra_indent, small_indent

if TYPE_CHECKING:
    from pygerber.gerber.ast.nodes import File

__all__ = [
    "Formatter",
    "extra_indent",
    "balanced",
    "small_indent",
    "MacroSplitMode",
    "MacroEndInNewLine",
    "FloatTrimTrailingZeros",
    "EmptyLineBeforePolaritySwitch",
    "KeepNonStandaloneCodes",
    "RemoveG54",
    "RemoveG55",
    "ExplicitParenthesis",
    "StripWhitespace",
    "Options",
]


def format(  # noqa: A001
    source: File, output: TextIO, options: Optional[Options] = None
) -> None:
    """Write formatted Gerber code based on given Abstract Syntax Tree to output IO.

    Parameters
    ----------
    source : File
        Gerber Abstract Syntax Tree to format.
    output : TextIO
        Output IO stream.
    options : Optional[Options], optional
        Formatter configuration options, by default None

    """
    Formatter(options=options).format(source, output)


def formats(source: File, options: Optional[Options] = None) -> str:
    """Return formatted Gerber code based on given Abstract Syntax Tree as string.

    Parameters
    ----------
    source : File
        Gerber Abstract Syntax Tree to format.
    options : Optional[Options], optional
        Formatter configuration options, by default None

    Returns
    -------
    str
        Formatted Gerber code

    """
    out = StringIO()
    format(source, out, options)
    return out.getvalue()
