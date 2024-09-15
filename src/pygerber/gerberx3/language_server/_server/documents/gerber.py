from __future__ import annotations

import hashlib
from typing import Optional

from pygerber.gerberx3.ast.nodes.file import File
from pygerber.gerberx3.language_server._server.documents.document import Document
from pygerber.gerberx3.language_server.status import is_language_server_available
from pygerber.gerberx3.parser.pyparsing.parser import Parser

if is_language_server_available():
    import lsprotocol.types as lspt  # noqa: TCH002
    from pygls.server import LanguageServer  # noqa: TCH002


def sha256(s: str) -> str:
    """Calculate SHA256 hash of the input."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class GerberDocument(Document):
    """The `GerberDocument` class represents a single Gerber X3 document."""

    def __init__(self, gls: LanguageServer) -> None:
        super().__init__(gls)
        self.parser = Parser()
        self.ast: Optional[File] = None
        self.source_hash = sha256("")
        self.uri = ""

    def load_ast_from_uri(self, uri: str) -> File:
        """Parse the input."""
        code = self.gls.workspace.get_document(uri)
        return self.load_ast_from_code(code.source)

    def load_ast_from_code(self, code: str) -> File:
        """Parse the input."""
        code_hash = sha256(code)

        if code_hash == self.source_hash and self.ast is not None:
            return self.ast

        self.ast = self.parser.parse(code)
        self.source_hash = sha256(code)

        self.log_info(f"Parsed AST for {self.uri} (sha256: {self.source_hash})")
        return self.ast

    async def on_open(self, params: lspt.DidOpenTextDocumentParams) -> None:
        """Handle the document open event."""
        self.uri = params.text_document.uri
        self.load_ast_from_code(params.text_document.text)

    async def on_close(self, params: lspt.DidCloseTextDocumentParams) -> None:
        """Handle the document close event."""

    async def on_change(self, params: lspt.DidChangeTextDocumentParams) -> None:
        """Handle the document change event."""
        self.load_ast_from_uri(params.text_document.uri)
