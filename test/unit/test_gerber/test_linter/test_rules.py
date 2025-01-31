from __future__ import annotations

from pygerber.gerber.ast.nodes import G54, G55, File
from pygerber.gerber.linter.linter import Linter
from pygerber.gerber.linter.rules import DEP001, DEP002


def test_DEP001() -> None:
    rule = DEP001()
    linter = Linter([rule])

    ast = File(nodes=[G54()])

    violations = linter.lint(ast)

    assert len(list(violations)) == 1


def test_DEP002() -> None:
    rule = DEP002()
    linter = Linter([rule])

    ast = File(nodes=[G55()])

    violations = linter.lint(ast)

    assert len(list(violations)) == 1
