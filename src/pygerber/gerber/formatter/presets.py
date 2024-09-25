"""The `presets` module contains named predefined formatter configurations."""

from __future__ import annotations

from pygerber.gerber.formatter.enums import (
    EmptyLineBeforePolaritySwitch,
    FloatTrimTrailingZeros,
    KeepNonStandaloneCodes,
    MacroEndInNewLine,
    MacroSplitMode,
    RemoveG54,
    RemoveG55,
    StripWhitespace,
)
from pygerber.gerber.formatter.options import Options

extra_indent = Options(
    indent_character=" ",
    macro_body_indent=4,
    macro_param_indent=0,
    macro_split_mode=MacroSplitMode.SplitOnPrimitives,
    macro_end_in_new_line=MacroEndInNewLine.Yes,
    block_aperture_body_indent=4,
    step_and_repeat_body_indent=4,
    float_decimal_places=6,
    float_trim_trailing_zeros=FloatTrimTrailingZeros.Yes,
    d01_indent=2,
    d02_indent=2,
    d03_indent=2,
    line_end="\n",
    empty_line_before_polarity_switch=EmptyLineBeforePolaritySwitch.Yes,
    keep_non_standalone_codes=KeepNonStandaloneCodes.SeparateCodes,
    remove_g54=RemoveG54.Remove,
    remove_g55=RemoveG55.Remove,
    strip_whitespace=StripWhitespace.Default,
)
balanced = Options(
    indent_character=" ",
    macro_body_indent=2,
    macro_param_indent=0,
    macro_split_mode=MacroSplitMode.SplitOnPrimitives,
    macro_end_in_new_line=MacroEndInNewLine.Yes,
    block_aperture_body_indent=2,
    step_and_repeat_body_indent=2,
    float_decimal_places=6,
    float_trim_trailing_zeros=FloatTrimTrailingZeros.Yes,
    d01_indent=0,
    d02_indent=0,
    d03_indent=0,
    line_end="\n",
    empty_line_before_polarity_switch=EmptyLineBeforePolaritySwitch.Yes,
    keep_non_standalone_codes=KeepNonStandaloneCodes.SeparateCodes,
    remove_g54=RemoveG54.Remove,
    remove_g55=RemoveG55.Remove,
    strip_whitespace=StripWhitespace.Default,
)

small_indent = Options(
    indent_character=" ",
    macro_body_indent=2,
    macro_param_indent=0,
    macro_split_mode=MacroSplitMode.SplitOnPrimitives,
    macro_end_in_new_line=MacroEndInNewLine.Yes,
    block_aperture_body_indent=2,
    step_and_repeat_body_indent=2,
    float_decimal_places=6,
    float_trim_trailing_zeros=FloatTrimTrailingZeros.Yes,
    d01_indent=0,
    d02_indent=0,
    d03_indent=0,
    line_end="\n",
    empty_line_before_polarity_switch=EmptyLineBeforePolaritySwitch.Yes,
    keep_non_standalone_codes=KeepNonStandaloneCodes.SeparateCodes,
    remove_g54=RemoveG54.Remove,
    remove_g55=RemoveG55.Remove,
    strip_whitespace=StripWhitespace.Default,
)
