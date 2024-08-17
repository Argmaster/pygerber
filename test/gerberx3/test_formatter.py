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

    assert formatted_ast.model_dump_json(serialize_as_any=True) == ast.model_dump_json(
        serialize_as_any=True
    )


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
