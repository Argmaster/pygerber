from typing import List, Type

from pygerber.tokens.token import Token

from .dnntoken import D01_Token, D02_Token, D03_Token
from .fstoken import FormatSpecifierToken
from .addtoken import ADD_Token

token_classes: List[Type[Token]] = [
    FormatSpecifierToken,
    D01_Token,
    D02_Token,
    D03_Token,
    ADD_Token,
]
