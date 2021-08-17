# -*- coding: utf-8 -*-
from typing import List, Type

from pygerber.tokens.token import Token

from .addtoken import ADD_Token
from .comment import G04Token, G74Token, G75Token
from .dnntoken import D01_Token, D02_Token, D03_Token
from .fstoken import FormatSpecifierToken

token_classes: List[Type[Token]] = [
    FormatSpecifierToken,
    D01_Token,
    D02_Token,
    D03_Token,
    ADD_Token,
    G04Token,
    G74Token,
    G75Token,
]
