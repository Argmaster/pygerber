from __future__ import annotations

from dataclasses import dataclass

import pytest

from pygerber.gerber.parser.pyparsing.parser import Parser
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
        "A64_OLinuXino_rev_G.*": Config(dpmm=40),
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
        "A64_OLinuXino_rev_G.*": Config(skip=True),
        "A64_OLinuXino_rev_G.A64-OlinuXino_Rev_G-B_Cu.gbr": Config(skip=False),
        "ATMEGA328-Motor-Board.*": Config(skip=True),
        "ATMEGA328-Motor-Board.ATMEGA328_Motor_Board-B.Cu.gbl": Config(skip=False),
        "expressions.*": Config(as_expression=True),
        **common_case_generator_config,
    },
    Config,
).parametrize


@parametrize
def test_pyparsing_parser_grammar(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip(reason=config.skip_reason)

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    parser = Parser()

    parser.parse(source)
