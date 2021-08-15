from typing import TYPE_CHECKING
from types import SimpleNamespace

from pygerber.tokens import FormatSpecifierToken

if TYPE_CHECKING:
    from pygerber.meta import Meta


class CoParser:

    format: FormatSpecifierToken

    def __init__(self) -> None:
        self.set_default_format()

    def set_default_format(self):
        default_format = "%FSDAX36Y36*%"
        dummy_meta = SimpleNamespace(ignore_deprecated=True)
        fstoken = FormatSpecifierToken.match(default_format)
        fstoken.dispatch(dummy_meta)
        self.format = fstoken

    def set_format(self, format: FormatSpecifierToken) -> None:
        self.format = format

    def parse(self, float_string: str) -> float:
        if float_string[0] == '-' or float_string[0] == '+':
            sign = float_string[0]
            float_string = float_string[1:]
        else:
            sign = ''
        float_with_zeros = f"{float_string:0>{self.format.length}}"
        float_int_part = float_with_zeros[:self.format.X_int]
        float_dec_part = float_with_zeros[self.format.X_int:]
        valid_float = f"{sign}{float_int_part}.{float_dec_part}"
        return float(valid_float)
