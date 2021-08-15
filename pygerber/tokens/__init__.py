from typing import List, Type

from pygerber.tokens.token import Token

from .dnntoken import D01_Token
from .fstoken import FormatSpecifierToken

token_classes: List[Type[Token]] = [FormatSpecifierToken, D01_Token]
