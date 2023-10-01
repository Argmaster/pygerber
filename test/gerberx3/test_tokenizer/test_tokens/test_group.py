from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.common.position import Position
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture

if TYPE_CHECKING:
    from test.conftest import AssetLoader


def test_find_closest_token(asset_loader: AssetLoader) -> None:
    ast = Tokenizer().tokenize(
        asset_loader.load_asset("gerberx3/expressions/AM/rounded-rect-0.grb").decode(
            "utf-8",
        ),
    )
    token = ast.find_closest_token(Position(22, 10))
    assert isinstance(token, DNNSelectAperture)
