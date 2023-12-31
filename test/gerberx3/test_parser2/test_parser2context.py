from __future__ import annotations

from test.gerberx3.test_parser2.common import parse_code

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID


def test_ensure_mutable_context() -> None:
    gerber_source = "D10*"

    initial_context = Parser2Context()
    initial_context.set_current_aperture_id(ApertureID("D11"))

    context = parse_code(gerber_source, initial_context)

    assert context is initial_context


def test_ensure_immutable_state() -> None:
    gerber_source = "D10*"

    initial_context = Parser2Context()
    initial_context.set_current_aperture_id(ApertureID("D11"))

    initial_state = initial_context.get_state()

    context = parse_code(gerber_source, initial_context)

    assert context.get_state() is not initial_state
