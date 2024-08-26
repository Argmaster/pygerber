from __future__ import annotations

from pathlib import Path

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.nodes.attribute.TF import TF_MD5
from pygerber.gerberx3.parser.pyparsing.parser import Parser


def test_check_source_hash() -> None:
    """Test check_source_hash."""
    source = Path("test/assets/gerberx3/AltiumGerberX2/PCB1_Profile.gbr").read_text()
    parser = Parser()

    output = parser.parse(source, strict=True)

    class CheckMD5(AstVisitor):
        def on_tf_md5(self, node: TF_MD5) -> None:
            assert node.check_source_hash() is True

    CheckMD5().on_file(output)
