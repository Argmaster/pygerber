from __future__ import annotations

from decimal import Decimal

from pygerber.gerberx3.parser2.parser2 import Parser2
from pygerber.gerberx3.renderer2.svg import SvgRenderer2, SvgRenderer2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

SOURCE = r"""
%FSLAX26Y26*%
%MOMM*%
%ADD100R,1.5X1.0X0.5*%
%ADD200C,1.5X1.0*%
%ADD300O,1.5X1.0X0.6*%
%ADD400P,1.5X3X5.0*%
D100*
X0Y0D03*
D200*
X0Y2000000D03*
D300*
X2000000Y0D03*
D400*
X2000000Y2000000D03*
M02*

"""


def render() -> None:
    stack = Tokenizer().tokenize(SOURCE)
    cmd_buf = Parser2().parse(stack)
    ref = SvgRenderer2(SvgRenderer2Hooks(scale=Decimal(10))).render(cmd_buf)
    ref.save_to("output.svg")


if __name__ == "__main__":
    render()
