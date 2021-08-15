from pygerber.tokens import FormatSpecifierToken


class CoParser:

    format: FormatSpecifierToken

    def __init__(self) -> None:
        self.set_format("FS")

    def set_format(self, format: FormatSpecifierToken) -> None:
        self.format = format

    def parse(self, float_string: str) -> float:
        pass
