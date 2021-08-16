from types import SimpleNamespace

from pygerber.tokens import FormatSpecifierToken


class CoParser:

    format: FormatSpecifierToken
    default_format = "%FSLAX36Y36*%"

    def __init__(self) -> None:
        self.set_default_format()

    def set_default_format(self):
        dummy_meta = SimpleNamespace(ignore_deprecated=True)
        fstoken = FormatSpecifierToken.match(
            self.default_format,
        )
        fstoken.dispatch(dummy_meta)
        self.format = fstoken

    def set_format(self, format: FormatSpecifierToken) -> None:
        self.format = format

    def parse(self, float_string: str) -> float:
        if float_string[0] == "-" or float_string[0] == "+":
            sign = float_string[0]
            float_string = float_string[1:]
        else:
            sign = ""
        # three possible behaviors of zeros
        float_with_zeros = self.format_zeros(float_string)
        float_int_part = float_with_zeros[: self.format.INT_FORMAT]
        float_dec_part = float_with_zeros[self.format.INT_FORMAT :]
        valid_float = f"{sign}{float_int_part}.{float_dec_part}"
        return float(valid_float)

    def format_zeros(self, float_string):
        # three possible behaviors of zeros
        if self.format.zeros == "L":  # skip leading
            return f"{float_string:0>{self.format.length}}"
        elif self.format.zeros == "T":  # skip trailing
            return f"{float_string:0<{self.format.length}}"
        else:  # D - don't skip, no oder gets through regex
            return float_string
