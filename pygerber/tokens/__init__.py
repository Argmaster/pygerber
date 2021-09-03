# -*- coding: utf-8 -*-
from typing import List, Type

from pygerber.tokens.token import Token

from .add import ADD_Token
from .comment import G04_Token, G74_Token, G75_Token, LoadName_Token
from .dnn import D01_Token, D02_Token, D03_Token, DNN_Loader_Token, G54DNN_Loader_Token
from .fs import FormatSpecifierToken
from .gnn import G0N_Token, G36_Token, G37_Token, G55_Token, G70_Token, G71_Token, G90_Token, G91_Token
from .load import (
    LoadPolarityToken,
    LoadMirroringToken,
    LoadRotationToken,
    LoadScalingToken,
    LoadUnitToken,
)
from .control import EndOfStream_Token, ImagePolarity_Token, Whitespace_Token
from .am import ApertureMacro_Token

token_classes: List[Type[Token]] = [
    Whitespace_Token,
    FormatSpecifierToken,
    D01_Token,
    D02_Token,
    D03_Token,
    DNN_Loader_Token,
    ADD_Token,
    G04_Token,
    G74_Token,
    G75_Token,
    G0N_Token,
    G36_Token,
    G37_Token,
    LoadPolarityToken,
    LoadMirroringToken,
    LoadRotationToken,
    LoadScalingToken,
    LoadUnitToken,
    EndOfStream_Token,
    ApertureMacro_Token,
    LoadName_Token,
    G54DNN_Loader_Token,
    G55_Token,
    G70_Token,
    G71_Token,
    G90_Token,
    G91_Token,
    ImagePolarity_Token,
]
