from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Any

import pytest

from pygerber.gerberx3.formatter import Formatter
from pygerber.gerberx3.parser.pyparsing.parser import Parser
from test.gerberx3.common import (
    GERBER_ASSETS_INDEX,
    Asset,
    CaseGenerator,
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


parametrize = CaseGenerator(
    GERBER_ASSETS_INDEX,
    {
        "A64-OLinuXino-rev-G.*": Config(dpmm=40),
        "flashes.*": Config(dpmm=40),
        "flashes.00_circle+h_4_tbh.grb": Config(
            xfail=True,
            xfail_message="Should warn, no mechanism implemented yet.",
        ),
        "ucamco.4.9.1.*": Config(dpmm=100),
        "ucamco.4.9.6.*": Config(dpmm=300),
        "ucamco.4.10.4.9.*": Config(dpmm=50),
        "ucamco.4.11.4.*": Config(dpmm=1),
        "expressions.*": Config(as_expression=True),
        **common_case_generator_config,
    },
    Config,
).parametrize


parametrize = CaseGenerator(
    GERBER_ASSETS_INDEX,
    {
        "A64-OLinuXino-rev-G.*": Config(skip=True),
        "A64-OLinuXino-rev-G.A64-OlinuXino_Rev_G-B_Cu.gbr": Config(skip=False),
        "ATMEGA328-Motor-Board.*": Config(skip=True),
        "ATMEGA328-Motor-Board.ATMEGA328_Motor_Board-B.Cu.gbl": Config(skip=False),
        "expressions.*": Config(as_expression=True),
        **common_case_generator_config,
    },
    Config,
).parametrize


@parametrize
def test_formatter(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip(reason=config.skip_reason)

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    parser = Parser()

    ast = parser.parse(source)
    output_buffer = StringIO()
    Formatter().format(ast, output_buffer)

    output_buffer.seek(0)
    formatted_source = output_buffer.read()

    formatted_ast = parser.parse(formatted_source)

    if formatted_ast.model_dump_json(serialize_as_any=True) != ast.model_dump_json(
        serialize_as_any=True
    ):
        msg = "Formatted AST is the same as the original AST."
        raise AssertionError(msg)


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
        macro_split_mode=Formatter.MacroSplitMode.PRIMITIVES,
        macro_end_in_new_line=False,
    )
    assert (
        formatted_source
        == """%AMDonut*
    1,1,$1,$2,$3*
    $4=($1x0.75)*
    1,0,$4,$2,$3*%
"""
    )


def _format(source: str, **kwargs: Any) -> str:
    ast = Parser().parse(source)
    output_buffer = StringIO()
    Formatter(**kwargs).format(ast, output_buffer)

    output_buffer.seek(0)
    return output_buffer.read()


def test_indent_character_tab() -> None:
    formatted_source = _format(
        DONUT_MACRO_SOURCE,
        indent_character="\t",
        macro_body_indent=1,
        macro_split_mode=Formatter.MacroSplitMode.PRIMITIVES,
        macro_end_in_new_line=False,
    )
    assert (
        formatted_source
        == """%AMDonut*
\t1,1,$1,$2,$3*
\t$4=($1x0.75)*
\t1,0,$4,$2,$3*%
"""
    )


class TestMacroSplitMode:
    def test_none(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_split_mode=Formatter.MacroSplitMode.NONE,
            macro_end_in_new_line=False,
        )
        assert (
            formatted_source
            == """%AMDonut*1,1,$1,$2,$3*$4=($1x0.75)*1,0,$4,$2,$3*%
"""
        )

    def test_primitives(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_split_mode=Formatter.MacroSplitMode.PRIMITIVES,
            macro_end_in_new_line=False,
        )
        assert (
            formatted_source
            == """%AMDonut*
    1,1,$1,$2,$3*
    $4=($1x0.75)*
    1,0,$4,$2,$3*%
"""
        )

    def test_parameters(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_param_indent=4,
            macro_split_mode=Formatter.MacroSplitMode.PARAMETERS,
            macro_end_in_new_line=False,
        )
        assert (
            formatted_source
            == """%AMDonut*
    1,
        1,
        $1,
        $2,
        $3*
    $4=($1x0.75)*
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
            macro_split_mode=Formatter.MacroSplitMode.NONE,
            macro_end_in_new_line=True,
        )
        assert (
            formatted_source
            == """%AMDonut*1,1,$1,$2,$3*$4=($1x0.75)*1,0,$4,$2,$3*
%
"""
        )

    def test_primitives__macro_end_in_new_line(self) -> None:
        formatted_source = _format(
            DONUT_MACRO_SOURCE,
            indent_character=" ",
            macro_body_indent=4,
            macro_param_indent=4,
            macro_split_mode=Formatter.MacroSplitMode.PRIMITIVES,
            macro_end_in_new_line=True,
        )
        assert (
            formatted_source
            == """%AMDonut*
    1,1,$1,$2,$3*
    $4=($1x0.75)*
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
            macro_split_mode=Formatter.MacroSplitMode.PARAMETERS,
            macro_end_in_new_line=True,
        )
        assert (
            formatted_source
            == """%AMDonut*
    1,
        1,
        $1,
        $2,
        $3*
    $4=($1x0.75)*
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
