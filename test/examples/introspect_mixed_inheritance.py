"""Example for introspection with selective inheritance from Parser2HooksBase and Parser2Hooks."""

from __future__ import annotations

from pygerber.gerberx3.parser2.attributes2 import ApertureAttributes
from pygerber.gerberx3.parser2.context2 import Parser2Context, Parser2ContextOptions
from pygerber.gerberx3.parser2.parser2 import (
    Parser2,
    Parser2OnErrorAction,
    Parser2Options,
)
from pygerber.gerberx3.parser2.parser2hooks import Parser2Hooks
from pygerber.gerberx3.parser2.parser2hooks_base import DefineAnyT, Parser2HooksBase
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer


class CustomHooks(Parser2HooksBase):
    def __init__(self) -> None:
        super().__init__()
        self.aperture_attributes: dict[ApertureID, ApertureAttributes] = {}

    class ApertureAttributeHooks(Parser2Hooks.ApertureAttributeHooks):
        pass

    class FileAttributeHooks(Parser2Hooks.FileAttributeHooks):
        pass

    class ObjectAttributeHooks(Parser2Hooks.ObjectAttributeHooks):
        pass

    class DeleteAttributeHooks(Parser2Hooks.DeleteAttributeHooks):
        pass

    class DefineApertureTokenHooks(Parser2HooksBase.DefineApertureTokenHooks):
        hooks: CustomHooks

        def on_parser_visit_token(
            self,
            token: DefineAnyT,
            context: Parser2Context,
        ) -> None:
            self.hooks.aperture_attributes[token.aperture_id] = (
                context.aperture_attributes
            )
            return super().on_parser_visit_token(token, context)


GERBER_SOURCE = r"""
%TF.GenerationSoftware,KiCad,Pcbnew,5.1.5-52549c5~84~ubuntu18.04.1*%
%TF.CreationDate,2020-02-11T15:54:30+02:00*%
%TF.ProjectId,A64-OlinuXino_Rev_G,4136342d-4f6c-4696-9e75-58696e6f5f52,G*%
%TF.SameCoordinates,Original*%
%TF.FileFunction,Copper,L6,Bot*%
%TF.FilePolarity,Positive*%
%FSLAX46Y46*%
G04 Gerber Fmt 4.6, Leading zero omitted, Abs format (unit mm)*
G04 Created by KiCad (PCBNEW 5.1.5-52549c5~84~ubuntu18.04.1) date 2020-02-11 15:54:30*
%MOMM*%
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

    for aperture, attributes in hooks.aperture_attributes.items():
        print(aperture)
        print(attributes)


if __name__ == "__main__":
    main()
