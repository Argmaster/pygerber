"""The `options` module contains definition of `Options` class."""

from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, Field

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


class Options(BaseModel):
    """The `Options` class aggregates configuration options for the Gerber
    formatter.

    For detailed description of individual options, please visit (TODO: Add doc link).
    """

    indent_character: Literal[" ", "\t"] = Field(default=" ")
    """Character used for indentation, by default " " (space)."""

    macro_body_indent: Union[str, int] = Field(default=0)
    """Indentation of macro body, could be either a string containing desired
    whitespaces or integer which will be used to create indent string based on
    `indent_character`, by default 0  which results in no indentation.
    """

    macro_param_indent: Union[str, int] = Field(default=0)
    """Indentation of macro parameters, could be either a string containing desired
    whitespaces or integer which will be used to create indent string based on
    `indent_character`, by default 0 which results in no indentation.

    `macro_param_indent` indentation is added on top of macro body indentation.

    `macro_param_indent` has effect only when `macro_split_mode` is `PARAMETERS`.
    """

    macro_split_mode: MacroSplitMode = Field(default=MacroSplitMode.SplitOnPrimitives)
    """Changes how macro definitions are formatted, by default
    `MacroSplitMode.SplitOnPrimitives`.

    ---

    When `NoSplit` is selected, macro definition will be formatted as a single line.

    ```gerber
    %AMDonut*1,1,$1,$2,$3*$4=$1x0.75*1,0,$4,$2,$3*%
    ```

    ---

    When `SplitOnPrimitives` is selected, macro definition will be formatted with each
    primitive in a new line.

    ```gerber
    %AMDonut*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    1,0,$4,$2,$3*%
    ```

    ---

    When `SplitOnParameters` is selected, macro definition will be formatted with each
    primitive on a new line and each parameter of a primitive on a new line.

    ```gerber
    %AMDonut*
    1,
    1,
    $1,
    $2,
    $3*
    $4=$1x0.75*
    1,
    0,
    $4,
    $2,
    $3*%
    ```

    Use `macro_body_indent` and `macro_param_indent` to control indentation.
    """

    macro_end_in_new_line: MacroEndInNewLine = Field(default=MacroEndInNewLine.No)
    """Toggles placing % sign which marks the end of macro in new line, by default
    `MacroEndInNewLine.No`
    """

    block_aperture_body_indent: Union[str, int] = Field(default=0)
    """Indentation of block aperture definition body, could be either a string
    containing desired whitespaces or integer which will be used to create indent
    string based `indent_character`, by default 0 which results in no indentation.

    This indentations stacks for nested block apertures.
    """

    step_and_repeat_body_indent: Union[str, int] = Field(default=0)
    """Indentation of step and repeat definition body, could be either a string
    containing desired whitespaces or integer which will be used to create indent
    string based `indent_character`, by default 0 which results in no indentation.

    This indentations stacks for nested step and repeat blocks.
    """

    float_decimal_places: int = Field(default=-1)
    """Limit number of decimal places shown for float values, by default -1 which means
    as many decimal places as needed.
    """

    float_trim_trailing_zeros: FloatTrimTrailingZeros = Field(
        default=FloatTrimTrailingZeros.Yes
    )
    """Remove trailing zeros from floats, by default `FloatTrimTrailingZeros.Yes`.

    When this is set to `FloatTrimTrailingZeros.Yes`, after floating point number is
    formatted with respect to `float_decimal_places`, trailing zeros are removed. If
    all zeros after decimal point are removed, decimal point is also removed.
    """

    d01_indent: Union[str, int] = Field(default=0)
    """Custom indentation of D01 command, could be either a string
    containing desired whitespaces or integer which will be used to create indent
    string based `indent_character`, by default 0
    """

    d02_indent: Union[str, int] = Field(default=0)
    """Custom indentation of D02 command, could be either a string
    containing desired whitespaces or integer which will be used to create indent
    string based `indent_character`, by default 0
    """

    d03_indent: Union[str, int] = Field(default=0)
    """Custom indentation of D03 command, could be either a string
    containing desired whitespaces or integer which will be used to create indent
    string based `indent_character`, by default 0
    """

    line_end: Literal["\n", "\r\n"] = Field(default="\n")
    """Line ending character, Unix or Windows style, by default "\n" (Unix style)
    If `strip_whitespace` is enabled, this setting is ignored and no line endings are
    added.
    """

    empty_line_before_polarity_switch: EmptyLineBeforePolaritySwitch = Field(
        default=EmptyLineBeforePolaritySwitch.No
    )
    """Add empty line before polarity switch, by default
    `EmptyLineBeforePolaritySwitch.Yes`

    Inserting empty lines before polarity switches enhances visual separation of
    sequences of commands with different polarities.
    """

    keep_non_standalone_codes: KeepNonStandaloneCodes = Field(
        default=KeepNonStandaloneCodes.Keep
    )
    """Keep non-standalone codes in the output, by default `KeepNonStandaloneCodes.Keep`

    If this option is disabled, legacy merged code forms like `G70D02*`
    will be divided into two separate commands, `G70*` and `D02*`, otherwise
    they will be kept as is.
    """

    remove_g54: RemoveG54 = Field(default=RemoveG54.Keep)
    """Remove G54 code from output, by default `RemoveG54.Keep`

    G54 code has no effect on the output, it was used in legacy files to
    prefix select aperture command.
    """

    remove_g55: RemoveG55 = Field(default=RemoveG55.Keep)
    """Remove G55 code from output, by default `RemoveG55.Keep`

    G55 code has no effect on the output, it was used in legacy files to
    prefix flash command.
    """

    explicit_parenthesis: ExplicitParenthesis = Field(
        default=ExplicitParenthesis.KeepOriginal
    )
    """Toggle explicit parenthesis around all mathematical expressions within macro, by
    default `ExplicitParenthesis.KeepOriginal`
    """

    strip_whitespace: StripWhitespace = Field(default=StripWhitespace.Default)
    """Toggle stripping of whitespace from the output, by default
    `StripWhitespace.Default` which results in normal whitespace handling.
    """
