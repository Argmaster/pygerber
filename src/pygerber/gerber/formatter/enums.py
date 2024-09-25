"""The `enums` module contains enumerations used in the Gerber X3 formatter."""

from __future__ import annotations

from enum import Enum


class MacroSplitMode(Enum):
    """Macro split mode."""

    NoSplit = "NoSplit"
    SplitOnPrimitives = "SplitOnPrimitives"
    SplitOnParameters = "SplitOnParameters"


class MacroEndInNewLine(Enum):
    """Macro end in new line."""

    Yes = "Yes"
    No = "No"


class FloatTrimTrailingZeros(Enum):
    """Float trim trailing zeros."""

    Yes = "Yes"
    No = "No"


class EmptyLineBeforePolaritySwitch(Enum):
    """Empty line before polarity switch."""

    Yes = "Yes"
    No = "No"


class KeepNonStandaloneCodes(Enum):
    """Keep non standalone codes."""

    SeparateCodes = "SeparateCodes"
    Keep = "Keep"


class RemoveG54(Enum):
    """Remove G54 command."""

    Remove = "Remove"
    Keep = "Keep"


class RemoveG55(Enum):
    """Remove G55 command."""

    Remove = "Remove"
    Keep = "Keep"


class ExplicitParenthesis(Enum):
    """Explicit parenthesis."""

    AddExplicit = "AddExplicit"
    KeepOriginal = "KeepOriginal"


class StripWhitespace(Enum):
    """Strip whitespace."""

    StripAll = "StripAll"
    Default = "Default"
