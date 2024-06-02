from __future__ import annotations

from dataclasses import dataclass
from test.gerberx3.common import GERBER_ASSETS_INDEX, Asset, CaseGenerator, ConfigBase

import pytest

from pygerber.gerberx3.parser2.parser2 import Parser2
from pygerber.gerberx3.renderer2.raster import RasterRenderer2, RasterRenderer2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer


@dataclass
class Config(ConfigBase):
    """Configuration for the test."""

    dpmm: int = 20
    as_expression: bool = False


@CaseGenerator[Config](
    GERBER_ASSETS_INDEX,
    {
        "*.A64-OLinuXino-rev-G.*": Config(dpmm=40),
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
        "incomplete.*": Config(skip=True),
    },
    Config,
).parametrize
def test_raster_renderer2(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip()

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    tokenizer = Tokenizer()

    if config.as_expression:
        stack = tokenizer.tokenize_expressions(source)
    else:
        stack = tokenizer.tokenize(source)

    parser = Parser2()
    cmd_buf = parser.parse(stack)

    ref = RasterRenderer2(RasterRenderer2Hooks(dpmm=config.dpmm)).render(cmd_buf)

    output_file_path = asset.get_output_file(".raster_renderer2").with_suffix(".png")
    ref.save_to(output_file_path)
