# -*- coding: utf-8 -*-
from typing import List
from typing import Type

from pygerber.tokens.token import Token

from .add import ADD_Token
from .am import ApertureMacro_Token
from .comment import G04_Token
from .comment import G74_Token
from .comment import G75_Token
from .comment import LoadName_Token
from .control import EndOfStream_Token
from .control import ImagePolarity_Token
from .control import Whitespace_Token
from .dnn import D01_Token
from .dnn import D02_Token
from .dnn import D03_Token
from .dnn import DNN_Loader_Token
from .dnn import G54DNN_Loader_Token
from .fs import FormatSpecifierToken
from .gnn import G0N_Token
from .gnn import G36_Token
from .gnn import G37_Token
from .gnn import G55_Token
from .gnn import G70_Token
from .gnn import G71_Token
from .gnn import G90_Token
from .gnn import G91_Token
from .load import LoadMirroringToken
from .load import LoadPolarityToken
from .load import LoadRotationToken
from .load import LoadScalingToken
from .load import LoadUnitToken

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
