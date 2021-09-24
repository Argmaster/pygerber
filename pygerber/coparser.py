# -*- coding: utf-8 -*-
from pygerber.exceptions import FeatureNotSupportedError
from pygerber.tokens import FormatSpecifierToken


class CoParser:

    format: FormatSpecifierToken
    default_format = "%FSLAX36Y36*%"

    def __init__(self) -> None:
        self.set_default_format()

    def set_default_format(self):
        re_match = FormatSpecifierToken.regex.match(
            self.default_format,
        )
        self.format = FormatSpecifierToken(re_match, None)

    def set_format(self, format: FormatSpecifierToken) -> None:
        self.format = format

    def set_mode(self, mode: str) -> None:
        self.format.mode = mode

    def get_mode(self) -> str:
        return self.format.mode

    def set_zeros(self, zeros: str) -> None:
        self.format.zeros = zeros

    def get_zeros(self) -> None:
        return self.format.zeros

    def dump(self, co: float) -> str:
        if co < 0:
            sign = "-"
            co = abs(co)
        else:
            sign = ""
        DEC_FORMAT = self.format.DEC_FORMAT
        integer_as_int = int(co)
        co_decimal_rounded = round(co - integer_as_int, DEC_FORMAT)
        decimal_as_int = int(co_decimal_rounded * 10 ** DEC_FORMAT)

        if self.get_zeros() == "L":
            if integer_as_int != 0:
                output = sign + str(integer_as_int)
                output += str(decimal_as_int).rjust(DEC_FORMAT, "0")
            else:
                output = sign + str(decimal_as_int)
            return output
        else:
            raise FeatureNotSupportedError(
                "Dump of other zeros format than 'L' not supported."
            )

    def parse(self, float_string: str) -> float:
        if float_string[0] == "-" or float_string[0] == "+":
            sign = float_string[0]
            float_string = float_string[1:]
        else:
            sign = ""
        float_with_zeros = self.format_zeros(float_string)
        float_int_part = float_with_zeros[: self.format.INT_FORMAT]
        float_dec_part = float_with_zeros[self.format.INT_FORMAT :]
        valid_float = f"{sign}{float_int_part}.{float_dec_part}"
        return float(valid_float)

    def format_zeros(self, float_string):
        # three possible behaviors of zeros
        if self.get_zeros() == "L":  # skip leading
            return f"{float_string:0>{self.format.length}}"
        elif self.get_zeros() == "T":
            return float_string # we don't need trailing zeros anyway
        else:
            return float_string # use as-is as no zeros are skipped
