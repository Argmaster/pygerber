from __future__ import annotations

from pathlib import Path
from test.gerberx3.test_parser2.common import debug_dump_context, parse_code
from unittest.mock import MagicMock

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.state_enums import Mirroring
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID

DEBUG_DUMP_DIR = Path(__file__).parent / ".output" / "test_parser2context"
DEBUG_DUMP_DIR.mkdir(exist_ok=True, parents=True)


def test_ensure_mutable_context() -> None:
    gerber_source = "D10*"

    initial_context = Parser2Context()
    initial_context.set_aperture(ApertureID("D10"), MagicMock())
    initial_context.set_current_aperture_id(ApertureID("D10"))

    context = parse_code(gerber_source, initial_context)

    assert context is initial_context


def test_ensure_immutable_state() -> None:
    gerber_source = "D10*"

    initial_context = Parser2Context()
    initial_context.set_aperture(ApertureID("D10"), MagicMock())
    initial_context.set_current_aperture_id(ApertureID("D10"))

    initial_state = initial_context.get_state()

    context = parse_code(gerber_source, initial_context)

    assert context.get_state() is not initial_state


def test_default_mirroring() -> None:
    context = Parser2Context()
    assert context.get_mirroring() is Mirroring.NoMirroring

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_default_mirroring.__qualname__,
    )
