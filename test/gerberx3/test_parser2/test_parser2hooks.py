from __future__ import annotations

from test.gerberx3.test_parser2.common import parse_code

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID


def test_begin_block_aperture_token_hooks() -> None:
    gerber_source = "%ABD10*%"

    initial_context = Parser2Context()
    initial_context.set_is_aperture_block(is_aperture_block=False)
    initial_context.set_aperture_block_id(None)

    context = parse_code(gerber_source, initial_context)

    assert context.get_is_aperture_block() is True
    assert context.get_aperture_block_id() == "D10"


def test_end_block_aperture_token_hooks() -> None:
    gerber_source = "%AB*%"

    initial_context = Parser2Context()
    initial_context.set_is_aperture_block(is_aperture_block=True)
    initial_context.set_aperture_block_id(ApertureID("D10"))

    context = parse_code(gerber_source, initial_context)

    assert context.get_is_aperture_block() is False
    assert context.get_aperture_block_id() is None


def test_select_aperture_token_hooks() -> None:
    gerber_source = "D10*"

    initial_context = Parser2Context()
    initial_context.set_current_aperture_id(ApertureID("D11"))

    context = parse_code(gerber_source, initial_context)

    assert context.get_current_aperture_id() == "D10"
