from __future__ import annotations

import hashlib
import re
from io import StringIO
from typing import Optional

from pygerber.gerber.ast.node_finder import NodeFinder, ZeroBasedPosition
from pygerber.gerber.ast.nodes import File, Invalid
from pygerber.gerber.ast.state_tracking_visitor import State, StateTrackingVisitor
from pygerber.gerber.formatter import Formatter
from pygerber.gerber.language_server._server.documents.document import Document
from pygerber.gerber.language_server._server.hover.gerber import GerberHoverCreator
from pygerber.gerber.language_server.status import is_language_server_available
from pygerber.gerber.parser.pyparsing.parser import Parser

if is_language_server_available():
    import lsprotocol.types as lspt
    from pygls.server import LanguageServer  # noqa: TCH002


def sha256(s: str) -> str:
    """Calculate SHA256 hash of the input."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class GerberDocument(Document):
    """The `GerberDocument` class represents a single Gerber X3 document."""

    def __init__(self, gls: LanguageServer) -> None:
        super().__init__(gls)
        self.flush_cached_values()

    def flush_cached_values(self) -> None:
        self.parser = Parser(resilient=True)
        self.ast: Optional[File] = None
        self.state: Optional[State] = None
        self.source_hash = sha256("")
        self.uri = ""
        self.cached_aperture_completion: Optional[lspt.CompletionList] = None

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
        self.flush_cached_values()
        self.uri = params.text_document.uri
        self.load_ast_from_code(params.text_document.text)

    async def on_close(self, params: lspt.DidCloseTextDocumentParams) -> None:
        """Handle the document close event."""

    async def on_change(self, params: lspt.DidChangeTextDocumentParams) -> None:
        """Handle the document change event."""
        self.flush_cached_values()
        self.load_ast_from_uri(params.text_document.uri)

    async def on_hover(self, params: lspt.HoverParams) -> lspt.Hover | None:
        """Handle the hover event."""
        position = ZeroBasedPosition(
            line=params.position.line, column=params.position.character
        ).to_one_based()

        if self.ast is None:
            return None

        node = NodeFinder(self.ast).find_node(position)

        if node is None:
            return None

        message = GerberHoverCreator(self.ast).create_hover_markdown(node)

        source_info = node.source_info
        if source_info is None:
            return None

        return lspt.Hover(
            contents=lspt.MarkupContent(value=message, kind=lspt.MarkupKind.Markdown),
            range=lspt.Range(
                start=lspt.Position(source_info.line - 1, source_info.column - 1),
                end=lspt.Position(source_info.end_line - 1, source_info.end_column - 1),
            ),
        )

    async def on_completion(
        self, params: lspt.CompletionParams
    ) -> lspt.CompletionList | None:
        """Handle the completion event."""
        if self.ast is None:
            return None

        position = ZeroBasedPosition(
            line=params.position.line, column=params.position.character
        ).to_one_based()
        node = NodeFinder(self.ast).find_node(position)
        self.gls.show_message_log(str(node))

        if not isinstance(node, Invalid) or len(node.string) == 0:
            return None

        if re.match(r"G\d*", node.string):
            return self.get_completion_g_codes()

        if re.match(r"D\d*", node.string):
            return self.get_completion_apertures()

        if re.match(r"%", node.string):
            return self.get_completion_extended_command()

        self.gls.show_message_log("No completion handler found.")
        return lspt.CompletionList(is_incomplete=False, items=[])

    def get_completion_apertures(self) -> lspt.CompletionList | None:
        """Get the list of apertures."""
        if self.cached_aperture_completion is not None:
            return self.cached_aperture_completion

        state = self.get_gerber_state()
        if state is None:
            return None

        aperture_completion = []

        formatter = Formatter()

        for name, node in state.apertures.apertures.items():
            out = StringIO()
            formatter.format(File(nodes=[node]), out)

            aperture_completion.append(
                lspt.CompletionItem(
                    label=name,
                    kind=lspt.CompletionItemKind.Function,
                    detail=out.getvalue(),
                )
            )

        for name, node in state.apertures.blocks.items():
            out = StringIO()
            formatter.format(File(nodes=[node.open]), out)

            aperture_completion.append(
                lspt.CompletionItem(
                    label=name,
                    kind=lspt.CompletionItemKind.Method,
                    detail=out.getvalue(),
                )
            )

        self.cached_aperture_completion = lspt.CompletionList(
            is_incomplete=False, items=aperture_completion
        )

        return self.cached_aperture_completion

    def get_gerber_state(self) -> Optional[State]:
        """Get the state of the document."""
        if self.state is None:
            visitor = StateTrackingVisitor(ignore_program_stop=True)
            if self.ast is None:
                return None

            self.ast.visit(visitor)
            self.state = visitor.state

        return self.state

    def get_completion_g_codes(self) -> lspt.CompletionList | None:
        """Get the list of G-codes."""
        return lspt.CompletionList(
            is_incomplete=False,
            items=[
                lspt.CompletionItem(
                    label="G01*",
                    kind=lspt.CompletionItemKind.Function,
                    detail="Set linear plot mode.",
                ),
                lspt.CompletionItem(
                    label="G02*",
                    kind=lspt.CompletionItemKind.Function,
                    detail="Set clockwise circular plot mode",
                ),
                lspt.CompletionItem(
                    label="G03*",
                    kind=lspt.CompletionItemKind.Function,
                    detail="Set counterclockwise circular plot mode",
                ),
                lspt.CompletionItem(
                    label="G04${1:comment}*",
                    kind=lspt.CompletionItemKind.Text,
                    detail="Add comment",
                    insert_text="G04${1:comment}*",
                    insert_text_format=lspt.InsertTextFormat.Snippet,
                ),
                lspt.CompletionItem(
                    label="G36*",
                    kind=lspt.CompletionItemKind.Function,
                    detail="Open region statement",
                ),
                lspt.CompletionItem(
                    label="G37*",
                    kind=lspt.CompletionItemKind.Function,
                    detail="Close region statement",
                ),
                lspt.CompletionItem(
                    label="G54",
                    kind=lspt.CompletionItemKind.Function,
                    detail="(Deprecated) Select aperture prefix",
                    deprecated=True,
                ),
                lspt.CompletionItem(
                    label="G55",
                    kind=lspt.CompletionItemKind.Function,
                    detail="(Deprecated) Prepare for flash",
                    deprecated=True,
                ),
                lspt.CompletionItem(
                    label="G74",
                    kind=lspt.CompletionItemKind.Function,
                    detail="(Deprecated) Set single quadrant mode",
                    deprecated=True,
                ),
                lspt.CompletionItem(
                    label="G75",
                    kind=lspt.CompletionItemKind.Function,
                    detail="Set multi quadrant mode",
                ),
                lspt.CompletionItem(
                    label="G90",
                    kind=lspt.CompletionItemKind.Function,
                    detail="(Deprecated) Set the `Coordinate format` to `Absolute notation`",
                    deprecated=True,
                ),
                lspt.CompletionItem(
                    label="G91",
                    kind=lspt.CompletionItemKind.Function,
                    detail="(Deprecated) Set the `Coordinate format` to `Incremental notation`",
                    deprecated=True,
                ),
            ],
        )

    def get_completion_extended_command(self) -> lspt.CompletionList | None:
        """Get the list of extended commands."""
        return lspt.CompletionList(
            is_incomplete=False,
            items=[
                *self._get_completion_ad_commands(),
                lspt.CompletionItem(
                    label="FSLAX46Y46*",
                    kind=lspt.CompletionItemKind.Function,
                    documentation="",
                    insert_text="FSLAX${1:4}${2:6}Y${1:4}${2:6}*",
                    insert_text_format=lspt.InsertTextFormat.Snippet,
                ),
                lspt.CompletionItem(
                    label="MOMM*",
                    kind=lspt.CompletionItemKind.Function,
                    documentation="",
                    insert_text="MO${1:MM}*",
                    insert_text_format=lspt.InsertTextFormat.Snippet,
                ),
                lspt.CompletionItem(
                    label="LPD*",
                    kind=lspt.CompletionItemKind.Function,
                    documentation="",
                    insert_text="LP${1:D}*",
                    insert_text_format=lspt.InsertTextFormat.Snippet,
                ),
                lspt.CompletionItem(
                    label="LPC*",
                    kind=lspt.CompletionItemKind.Function,
                    documentation="",
                    insert_text="LP${1:C}*",
                    insert_text_format=lspt.InsertTextFormat.Snippet,
                ),
            ],
        )

    def _get_completion_ad_commands(self) -> list[lspt.CompletionItem]:
        """Get the list of AD commands."""
        state = self.get_gerber_state()
        if state is None:
            return []

        next_code = state.apertures.get_next_free_aperture_code()

        return [
            lspt.CompletionItem(
                label=string,
                kind=lspt.CompletionItemKind.Constructor,
                documentation=doc,
                insert_text=string,
                insert_text_format=lspt.InsertTextFormat.Snippet,
            )
            for string, doc in [
                (
                    f"ADD{next_code}C,${{1:diameter}}*",
                    "Add circle aperture definition",
                ),
                (
                    f"ADD{next_code}C,${{1:diameter}}X${{2:hole_diameter}}*",
                    "Add circle aperture definition",
                ),
                (
                    f"ADD{next_code}R,${{1:width}}X${{2:height}}*",
                    "Add rectangle aperture definition",
                ),
                (
                    f"ADD{next_code}R,${{1:width}}X${{2:height}}X${{3:hole_diameter}}*",
                    "Add rectangle aperture definition",
                ),
                (
                    f"ADD{next_code}O,${{1:width}}X${{2:height}}*",
                    "Add obround aperture definition",
                ),
                (
                    f"ADD{next_code}O,${{1:width}}X${{2:height}}X${{3:hole_diameter}}*",
                    "Add obround aperture definition",
                ),
                (
                    f"ADD{next_code}P,${{1:outer_diameter}}X${{2:vertices}}X${{3:rotation}}*",
                    "Add polygon aperture definition",
                ),
                (
                    f"ADD{next_code}P,${{1:outer_diameter}}X${{2:vertices}}X${{3:rotation}}X${{4:hole_diameter}}*",
                    "Add polygon aperture definition",
                ),
            ]
        ]
