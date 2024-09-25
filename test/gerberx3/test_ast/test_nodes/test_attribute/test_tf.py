from __future__ import annotations

from pathlib import Path

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.nodes.attribute.TF import TF_MD5
from pygerber.gerber.parser.pyparsing.parser import Parser


def test_check_source_hash() -> None:
    """Test check_source_hash."""
    source = Path("test/assets/gerberx3/AltiumGerberX2/PCB1_Profile.gbr").read_text()
    parser = Parser()

    output = parser.parse(source, strict=True)

    class CheckMD5(AstVisitor):
        def on_tf_md5(self, node: TF_MD5) -> TF_MD5:
            assert node.check_source_hash() is True
            return node

    CheckMD5().on_file(output)
