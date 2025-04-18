from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Any

from pygerber.gerber.formatter import Formatter
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
from pygerber.gerber.formatter.options import Options
from pygerber.gerber.parser.pyparsing.parser import Parser
from test.unit.test_gerber.common import (
    ConfigBase,
)


@dataclass
class Config(ConfigBase):
    """Configuration for the test."""

    dpmm: int = 20
    as_expression: bool = False
    compare_with_reference: bool = True


common_case_generator_config = {
    "macro.*": Config(dpmm=100),
    "incomplete.*": Config(skip=True),
}


DONUT_MACRO_SOURCE = """%AMDonut*
1,1,$1,$2,$3*
$4=$1x0.75*
1,0,$4,$2,$3*
%
"""


def test_indent_character_space() -> None:
    formatted_source = _format(
        DONUT_MACRO_SOURCE,
        indent_character=" ",
        macro_body_indent=4,
        macro_split_mode=MacroSplitMode.SplitOnPrimitives,
        macro_end_in_new_line=False,
    )
    assert (
        formatted_source
        == """%AMDonut*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    1,0,$4,$2,$3*%
"""
    )


def _format(source: str, **kwargs: Any) -> str:
    ast = Parser().parse(source)
    output_buffer = StringIO()

    formatter_options = Options(
        indent_character=" ",
        macro_body_indent=0,
        macro_param_indent=0,
        macro_split_mode=MacroSplitMode.SplitOnPrimitives,
        macro_end_in_new_line=MacroEndInNewLine.No,
        block_aperture_body_indent=0,
        step_and_repeat_body_indent=0,
        float_decimal_places=6,
        float_trim_trailing_zeros=FloatTrimTrailingZeros.Yes,
        d01_indent=0,
        d02_indent=0,
        d03_indent=0,
        line_end="\n",
        empty_line_before_polarity_switch=EmptyLineBeforePolaritySwitch.No,
        keep_non_standalone_codes=KeepNonStandaloneCodes.Keep,
        remove_g54=RemoveG54.Keep,
        remove_g55=RemoveG55.Keep,
        explicit_parenthesis=ExplicitParenthesis.KeepOriginal,
        strip_whitespace=StripWhitespace.Default,
    )
    formatter_options = formatter_options.model_copy(update=kwargs)
    Formatter(options=formatter_options).format(ast, output_buffer)  # type: ignore[arg-type]

    output_buffer.seek(0)
    return output_buffer.read()


def test_indent_character_tab() -> None:
    formatted_source = _format(
        DONUT_MACRO_SOURCE,
        indent_character="\t",
        macro_body_indent=1,
        macro_split_mode=MacroSplitMode.SplitOnPrimitives,
        macro_end_in_new_line=False,
    )
    assert (
        formatted_source
        == """%AMDonut*
\t1,1,$1,$2,$3*
\t$4=$1x0.75*
\t1,0,$4,$2,$3*%
"""
    )


class TestMacroSplitMode:
    def test_none(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_split_mode=MacroSplitMode.NoSplit,
            macro_end_in_new_line=MacroEndInNewLine.No,
        )
        assert (
            formatted_source
            == """%AMDonut*1,1,$1,$2,$3*$4=$1x0.75*1,0,$4,$2,$3*%
"""
        )

    def test_primitives(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_split_mode=MacroSplitMode.SplitOnPrimitives,
            macro_end_in_new_line=MacroEndInNewLine.No,
        )
        assert (
            formatted_source
            == """%AMDonut*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    1,0,$4,$2,$3*%
"""
        )

    def test_parameters(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_param_indent=4,
            macro_split_mode=MacroSplitMode.SplitOnParameters,
            macro_end_in_new_line=MacroEndInNewLine.No,
        )
        assert (
            formatted_source
            == """%AMDonut*
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
"""
        )

    def test_none__macro_end_in_new_line(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_param_indent=4,
            macro_split_mode=MacroSplitMode.NoSplit,
            macro_end_in_new_line=MacroEndInNewLine.Yes,
        )
        assert (
            formatted_source
            == """%AMDonut*1,1,$1,$2,$3*$4=$1x0.75*1,0,$4,$2,$3*
%
"""
        )

    def test_primitives__macro_end_in_new_line(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_param_indent=4,
            macro_split_mode=MacroSplitMode.SplitOnPrimitives,
            macro_end_in_new_line=MacroEndInNewLine.Yes,
        )
        assert (
            formatted_source
            == """%AMDonut*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    1,0,$4,$2,$3*
%
"""
        )

    def test_parameters_macro_end_in_new_line(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_param_indent=4,
            macro_split_mode=MacroSplitMode.SplitOnParameters,
            macro_end_in_new_line=MacroEndInNewLine.Yes,
        )
        assert (
            formatted_source
            == """%AMDonut*
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
        $3*
%
"""
        )


APERTURE_BLOCK_SOURCE = """%ABD12*%
%ADD11C,0.5*%
D10*
G01*
X-2500000Y-1000000D03*
Y1000000D03*
D11*
X-2500000Y-1000000D03*
X-500000Y-1000000D02*
X2500000D01*
G75*
G03*
X500000Y1000000I-2000000J0D01*
G01*
%AB*%
"""

APERTURE_BLOCK_NESTED_SOURCE = """%ABD102*%
G04 Define nested block aperture 101, consisting of 2x2 flashes of aperture 100*
%ABD101*%
D100*
X0Y0D03*
X0Y70000000D03*
X100000000Y0D03*
X100000000Y70000000D03*
%AB*%
D101*
X0Y0D03*
X0Y160000000D03*
X0Y320000000D03*
X230000000Y0D03*
X230000000Y160000000D03*
X230000000Y320000000D03*
D12*
X19500000Y-10000000D03*
%AB*%
"""


def test_block_aperture_body_indent() -> None:
    formatted_source = _format(
        APERTURE_BLOCK_SOURCE,
        indent_character=" ",
        block_aperture_body_indent=4,
    )
    assert (
        formatted_source
        == """%ABD12*%
    %ADD11C,0.5*%
    D10*
    G01*
    X-2500000Y-1000000D03*
    Y1000000D03*
    D11*
    X-2500000Y-1000000D03*
    X-500000Y-1000000D02*
    X2500000D01*
    G75*
    G03*
    X500000Y1000000I-2000000J0D01*
    G01*
%AB*%
"""
    )


def test_nested_block_aperture_body_indent() -> None:
    formatted_source = _format(
        APERTURE_BLOCK_NESTED_SOURCE,
        indent_character=" ",
        block_aperture_body_indent=4,
    )
    assert (
        formatted_source
        == """%ABD102*%
    G04 Define nested block aperture 101, consisting of 2x2 flashes of aperture 100*
    %ABD101*%
        D100*
        X0Y0D03*
        X0Y70000000D03*
        X100000000Y0D03*
        X100000000Y70000000D03*
    %AB*%
    D101*
    X0Y0D03*
    X0Y160000000D03*
    X0Y320000000D03*
    X230000000Y0D03*
    X230000000Y160000000D03*
    X230000000Y320000000D03*
    D12*
    X19500000Y-10000000D03*
%AB*%
"""
    )


STEP_AND_REPEAT_SOURCE = """%SRX3Y2I5.0J4.0*%
D13*
X123456Y789012D03*
D14*
X456789Y012345D03*
%SR*%
"""


def test_step_and_repeat_body_indent() -> None:
    formatted_source = _format(
        STEP_AND_REPEAT_SOURCE,
        indent_character=" ",
        step_and_repeat_body_indent=4,
    )
    from pathlib import Path

    Path("formatted.gbr").write_text(formatted_source)
    assert (
        formatted_source
        == """%SRX3Y2I5.0J4.0*%
    D13*
    X123456Y789012D03*
    D14*
    X456789Y012345D03*
%SR*%
"""
    )


AM_TEST1 = """%AMTEST1*
$2=100-$1/1.75+$2*
%
"""


def test_explicit_parenthesis() -> None:
    formatted_source = _format(
        AM_TEST1,
        explicit_parenthesis=ExplicitParenthesis.AddExplicit,
    )
    assert (
        formatted_source
        == """%AMTEST1*
$2=((100-($1/1.75))+$2)*%
"""
    )


def test_no_explicit_parenthesis() -> None:
    formatted_source = _format(
        AM_TEST1,
        explicit_parenthesis=ExplicitParenthesis.KeepOriginal,
    )
    assert (
        formatted_source
        == """%AMTEST1*
$2=100-$1/1.75+$2*%
"""
    )


def test_no_explicit_parenthesis_keep_original_same_order() -> None:
    """Check if parenthesis are kept the way they were in the original source
    while explicit_parenthesis is False and presence of parenthesis does not
    affect expression execution order.
    """
    formatted_source = _format(
        """%AMTEST1*
$2=100-($1/1.75)+$2*%
""",
        explicit_parenthesis=ExplicitParenthesis.KeepOriginal,
    )
    assert (
        formatted_source
        == """%AMTEST1*
$2=100-($1/1.75)+$2*%
"""
    )


def test_no_explicit_parenthesis_keep_original_different_order() -> None:
    """Check if parenthesis are kept the way they were in the original source
    while explicit_parenthesis is False and presence of parenthesis does
    affect expression execution order.
    """
    formatted_source = _format(
        """%AMTEST1*
$2=(100-$1)/1.75+$2*%
""",
        explicit_parenthesis=ExplicitParenthesis.KeepOriginal,
    )
    assert (
        formatted_source
        == """%AMTEST1*
$2=(100-$1)/1.75+$2*%
"""
    )
