from __future__ import annotations

from typing import Any, Optional

import pytest

from pygerber.gerberx3.ast.node_finder import NodeFinder, OneBasedPosition
from pygerber.gerberx3.ast.nodes import (
    AD,
    D03,
    FS,
    M02,
    MO,
    AMopen,
    Code1,
    Dnn,
    Node,
    SRclose,
    SRopen,
)
from pygerber.gerberx3.ast.nodes.math.constant import Constant
from pygerber.gerberx3.parser import parse
from test.assets.gerberx3.flashes import Flashes
from test.assets.gerberx3.macro.codes import MacroCodeAssets
from test.assets.gerberx3.step_and_repeat import StepAndRepeatAssets


class TestFindNode:
    @pytest.mark.parametrize(
        ("line", "column", "expect"),
        [(1, 1, FS), (3, 8, AD), (8, 5, D03), (6, 15, AD), (15, 3, M02)],
    )
    def test_circle_4_grb(self, line: int, column: int, expect: type[Node]) -> None:
        source = Flashes.asset_00_circle_4_grb.load()
        ast = parse(source)
        node = NodeFinder(ast).find_node(OneBasedPosition(line=line, column=column))
        assert isinstance(node, expect)

    @pytest.mark.parametrize(
        ("line", "column", "expect"),
        [
            (1, 1, FS),
            (1, 17, MO),
            (3, 17, Dnn),
            (5, 15, Dnn),
            (5, 19, Dnn),
            (5, 20, D03),
        ],
    )
    def test_circle_4_node_finder_grb(
        self, line: int, column: int, expect: type[Node]
    ) -> None:
        source = Flashes.asset_00_circle_4_node_finder_grb.load()
        ast = parse(source)
        node = NodeFinder(ast).find_node(OneBasedPosition(line=line, column=column))
        assert isinstance(node, expect)

    @pytest.mark.parametrize(
        ("line", "column", "expect", "fields"),
        [
            (1, 1, FS, None),
            (2, 1, MO, None),
            (5, 1, AMopen, None),
            (6, 3, AMopen, None),
            (6, 18, Code1, None),
            (9, 3, None, None),
            (9, 5, Code1, {"rotation": Constant(constant=45.0)}),
            (9, 17, Code1, {"rotation": Constant(constant=45.0)}),
            (9, 28, Code1, {"rotation": Constant(constant=45.0)}),
        ],
    )
    def test_macro_code_1(
        self,
        line: int,
        column: int,
        expect: Optional[type[Node]],
        fields: Optional[dict[str, Any]],
    ) -> None:
        source = MacroCodeAssets.code_1.load()
        ast = parse(source)
        node = NodeFinder(ast).find_node(OneBasedPosition(line=line, column=column))
        if expect is not None:
            assert isinstance(node, expect)
            if fields:
                for key, value in fields.items():
                    assert getattr(node, key) == value
        else:
            assert node is None

    @pytest.mark.parametrize(
        ("line", "column", "expect"),
        [
            (1, 1, FS),
            (5, 7, SRopen),
            (7, 8, D03),
            (9, 18, D03),
            (10, 1, SRclose),
        ],
    )
    def test_step_and_repeat(self, line: int, column: int, expect: type[Node]) -> None:
        source = StepAndRepeatAssets.cr_x_3.load()
        ast = parse(source)
        node = NodeFinder(ast).find_node(OneBasedPosition(line=line, column=column))
        assert isinstance(node, expect)
