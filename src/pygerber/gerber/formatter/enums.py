"""The `enums` module contains enumerations used in the Gerber X3 formatter."""

from __future__ import annotations

from enum import Enum


class MacroSplitMode(Enum):
    """Macro split mode."""

    NoSplit = "NoSplit"
    """Disable macro definition splitting."""

    SplitOnPrimitives = "SplitOnPrimitives"
    """Enable splitting macro definition on primitives."""

    SplitOnParameters = "SplitOnParameters"
    """Enable splitting macro definition on primitive parameters."""


class MacroEndInNewLine(Enum):
    """Macro end in new line."""

    Yes = "Yes"
    """Move % sign ending macro to new line."""

    No = "No"
    """keep % sign in same line as last primitive."""


class FloatTrimTrailingZeros(Enum):
    """Float trim trailing zeros."""

    Yes = "Yes"
    """Enable trimming of trailing zeros."""

    No = "No"
    """Disable trimming of trailing zeros."""


class EmptyLineBeforePolaritySwitch(Enum):
    """Empty line before polarity switch."""

    Yes = "Yes"
    """Enable adding empty line before polarity switch."""

    No = "No"
    """Disable adding empty line before polarity switch."""


class KeepNonStandaloneCodes(Enum):
    """Keep non standalone codes."""

    SeparateCodes = "SeparateCodes"
    """Separate non standalone codes into standalone equivalents."""

    Keep = "Keep"
    """Keep non standalone codes as they are."""


class RemoveG54(Enum):
    """Remove G54 command."""

    Remove = "Remove"
    """Remove G54 command from output."""

    Keep = "Keep"
    """Keep G54 command in output."""


class RemoveG55(Enum):
    """Remove G55 command."""

    Remove = "Remove"
    """Remove G55 command from output."""

    Keep = "Keep"
    """Keep G55 command in output."""


class ExplicitParenthesis(Enum):
    """Explicit parenthesis."""

    AddExplicit = "AddExplicit"
    """Add explicit parenthesis to all mathematical operations."""

    KeepOriginal = "KeepOriginal"
    """Keep original parenthesis in mathematical operations."""


class StripWhitespace(Enum):
    """Strip whitespace."""

    StripAll = "StripAll"
    """Strip all whitespace from the output."""

    Default = "Default"
    """Use implicit whitespace rules and those defined by other options."""
