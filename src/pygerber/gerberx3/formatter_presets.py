"""`pygerber.gerberx3.formatter_presets` module contains named predefined formatter
configurations.
"""

from __future__ import annotations

from pygerber.gerberx3.formatter import Formatter

extra_indent = {
    "indent_character": " ",
    "macro_body_indent": 4,
    "macro_param_indent": 0,
    "macro_split_mode": Formatter.MacroSplitMode.PRIMITIVES,
    "macro_end_in_new_line": True,
    "block_aperture_body_indent": 4,
    "step_and_repeat_body_indent": 4,
    "float_decimal_places": 6,
    "float_trim_trailing_zeros": True,
    "d01_indent": 2,
    "d02_indent": 2,
    "d03_indent": 2,
    "line_end": "\n",
    "empty_line_before_polarity_switch": True,
    "keep_non_standalone_codes": False,
    "remove_g54": True,
    "remove_g55": True,
    "strip_whitespace": False,
}
balanced = {
    "indent_character": " ",
    "macro_body_indent": 4,
    "macro_param_indent": 0,
    "macro_split_mode": Formatter.MacroSplitMode.PRIMITIVES,
    "macro_end_in_new_line": True,
    "block_aperture_body_indent": 4,
    "step_and_repeat_body_indent": 4,
    "float_decimal_places": 6,
    "float_trim_trailing_zeros": True,
    "d01_indent": 0,
    "d02_indent": 0,
    "d03_indent": 0,
    "line_end": "\n",
    "empty_line_before_polarity_switch": True,
    "keep_non_standalone_codes": False,
    "remove_g54": True,
    "remove_g55": True,
    "strip_whitespace": False,
}
small_indent = {
    "indent_character": " ",
    "macro_body_indent": 2,
    "macro_param_indent": 0,
    "macro_split_mode": Formatter.MacroSplitMode.PRIMITIVES,
    "macro_end_in_new_line": True,
    "block_aperture_body_indent": 2,
    "step_and_repeat_body_indent": 2,
    "float_decimal_places": 6,
    "float_trim_trailing_zeros": True,
    "d01_indent": 0,
    "d02_indent": 0,
    "d03_indent": 0,
    "line_end": "\n",
    "empty_line_before_polarity_switch": True,
    "keep_non_standalone_codes": False,
    "remove_g54": True,
    "remove_g55": True,
    "strip_whitespace": False,
}
