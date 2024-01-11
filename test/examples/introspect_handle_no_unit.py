"""Example for introspection with selective inheritance from IHooks and Parser2Hooks."""
from __future__ import annotations

from pygerber.gerberx3.parser2.context2 import Parser2Context, Parser2ContextOptions
from pygerber.gerberx3.parser2.errors2 import Parser2Error, UnitNotSet2Error
from pygerber.gerberx3.parser2.parser2 import (
    Parser2,
    Parser2OnErrorAction,
    Parser2Options,
)
from pygerber.gerberx3.parser2.parser2hooks import Parser2Hooks
from pygerber.gerberx3.state_enums import Unit
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer


class CustomHooks(Parser2Hooks):
    def on_parser_error(self, context: Parser2Context, error: Parser2Error) -> None:
        if isinstance(error, UnitNotSet2Error):
            context.set_draw_units(Unit.Inches)
        return super().on_parser_error(context, error)


GERBER_SOURCE = r"""
%FSLAX46Y46*%
G04 Let's not include MO command. *
%LPD*%
G04 APERTURE LIST*
%TA.AperFunction,EtchedComponent*%
%ADD10C,0.508000*%
%TD*%
%TA.AperFunction,EtchedComponent*%
%ADD11C,0.254000*%
%TD*%
%TA.AperFunction,ComponentPad*%
%ADD12O,2.800000X2.000000*%
%TD*%
%TA.AperFunction,ComponentPad*%
%ADD13C,1.650000*%
M02*
"""


def main() -> None:
    tokenizer = Tokenizer()
    ast = tokenizer.tokenize(GERBER_SOURCE)
    hooks = CustomHooks()
    parser = Parser2(
        Parser2Options(
            context_options=Parser2ContextOptions(hooks=hooks),
            on_update_drawing_state_error=Parser2OnErrorAction.UseHook,
        ),
    )
    parser.parse(ast)


if __name__ == "__main__":
    main()
