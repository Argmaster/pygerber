"""Example for introspection with selective inheritance from Parser2HooksBase and Parser2Hooks."""
from __future__ import annotations

from pygerber.gerberx3.parser2.context2 import Parser2Context, Parser2ContextOptions
from pygerber.gerberx3.parser2.parser2 import Parser2, Parser2Options
from pygerber.gerberx3.parser2.parser2hooks import Parser2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.g04_comment import Comment


class CustomHooks(Parser2Hooks):
    def __init__(self) -> None:
        super().__init__()
        self.comments: list[str] = []

    class CommentTokenHooks(Parser2Hooks.CommentTokenHooks):
        hooks: CustomHooks

        def on_parser_visit_token(
            self,
            token: Comment,
            context: Parser2Context,
        ) -> None:
            self.hooks.comments.append(token.content)
            return super().on_parser_visit_token(token, context)


GERBER_SOURCE = r"""
G04 Ucamco ex. 2: Shapes*           G04 A comment                                                            *
G04 Ucamco ex. 2: Shapes*           G04 Comment                                                              *
%MOMM*%                             G04 Units are mm                                                         *
%FSLAX36Y36*%                       G04 Format specification:                                                *
                                    G04  Leading zeros omitted                                               *
                                    G04  Absolute coordinates                                                *
                                    G04  Coordinates in 3 integer and 6 fractional digits.                   *
%TF.FileFunction,Other,Sample*%     G04 Attribute: the is not a PCB layer, it is just an                     *
                                    G04 example                                                              *
G04 Define Apertures*               G04 Comment                                                              *
%AMTHERMAL80*                       G04 Define the aperture macro 'THERMAL80'                                *
7,0,0,0.800,0.550,0.125,45*%        G04 Use thermal primitive in the macro                                   *
%ADD10C,0.1*%                       G04 Define aperture 10 as a circle with diameter 0.1 mm                  *
%ADD11C,0.6*%                       G04 Define aperture 11 as a circle with diameter 0.6 mm                  *
%ADD12R,0.6X0.6*%                   G04 Define aperture 12 as a rectangle with size 0.6 x 0.6 mm             *
%ADD13R,0.4X1.00*%                  G04 Define aperture 13 as a rectangle with size 0.4 x 1 mm               *
%ADD14R,1.00X0.4*%                  G04 Define aperture 14 as a rectangle with size 1 x 0.4 mm               *
%ADD15O,0.4X01.00*%                 G04 Define aperture 15 as an obround with size 0.4 x 1 mm                *
%ADD16P,1.00X3*%                    G04 Define aperture 16 as a polygon with 3 vertices and                  *
                                    G04 circumscribed circle with diameter 1 mm                              *
%ADD19THERMAL80*%                   G04 Define aperture 19 as an instance of macro aperture                  *
                                    G04 'THERMAL80' defined earlier                                          *
G04 Start image generation*         G04 A comment                                                            *
D10*                                G04 Select aperture 10 as current aperture                               *
X0Y2500000D02*                      G04 Set the current point to (0, 2.5) mm                                 *
G01*                                G04 Set linear plot mode                                                 *
X0Y0D01*                            G04 Create draw with the current aperture                                *
X2500000Y0D01*                      G04 Create draw with the current aperture                                *
X10000000Y10000000D02*              G04 Set the current point                                                *
X15000000D01*                       G04 Create draw with the current aperture                                *
X20000000Y15000000D01*              G04 Create draw with the current aperture                                *
X25000000D02*                       G04 Set the current point.                                               *
Y10000000D01*                       G04 Create draw with the current aperture                                *
D11*                                G04 Select aperture 11 as current aperture                               *
X10000000Y10000000D03*              G04 Create flash with the current aperture (11) at (10, 10).             *
X20000000D03*                       G04 Create a flash with the current aperture at (20, 10).                *
M02*                                G04 End of file                                                          *
"""


def main() -> None:
    tokenizer = Tokenizer()
    ast = tokenizer.tokenize(GERBER_SOURCE)
    hooks = CustomHooks()
    parser = Parser2(
        Parser2Options(context_options=Parser2ContextOptions(hooks=hooks)),
    )
    parser.parse(ast)

    for comment in hooks.comments:
        print(comment)


if __name__ == "__main__":
    main()
