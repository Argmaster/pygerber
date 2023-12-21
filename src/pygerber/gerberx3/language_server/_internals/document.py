from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

import lsprotocol.types as lspt

from pygerber.common.position import Position
from pygerber.gerberx3.language_server._internals.errors import EmptyASTError
from pygerber.gerberx3.linter.diagnostic import Diagnostic
from pygerber.gerberx3.parser.parser import StatePreservingParser
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from pygls.server import LanguageServer


class Document:
    """Represents single snapshot of a document."""

    def __init__(self, ls: LanguageServer, source: str, uri: str) -> None:
        self.ls = ls
        self.source = source
        self.uri = uri

        self.tokenizer = Tokenizer()

        self.ls.show_message_log(
            f"Created tokenizer for {uri}",
            lspt.MessageType.Info,
        )

        self.parser = StatePreservingParser()
        self.ls.show_message_log(
            f"Created parser for {uri}",
            lspt.MessageType.Info,
        )

        self.ls.show_message_log(
            f"Started tokenizing {uri}",
            lspt.MessageType.Info,
        )
        self.ast = self.tokenizer.tokenize_resilient(self.source)
        self.ls.show_message_log(
            f"Finished tokenizing {uri}",
            lspt.MessageType.Info,
        )

        self.ls.show_message_log(
            f"Started parsing {uri}",
            lspt.MessageType.Info,
        )
        self.parser.parse(self.ast)
        self.ls.show_message_log(
            f"Finished parsing {self.uri}",
            lspt.MessageType.Info,
        )

    def text_document_hover(self, params: lspt.HoverParams) -> Optional[lspt.Hover]:
        try:
            ast = self.ast
            token_accessor = ast.find_closest_token(
                Position.from_vscode_position(
                    params.position.line,
                    params.position.character,
                ),
            )
            if (token := token_accessor.token) is not None:
                logging.info(
                    "Found token for hover location %s, %s",
                    params.position,
                    token.get_token_position(),
                )

                return lspt.Hover(
                    contents=lspt.MarkupContent(
                        kind=lspt.MarkupKind.Markdown,
                        value=token.get_hover_message(self.parser.get_state_at(token)),
                    ),
                )

            logging.info(
                "Missing token for hover location %s",
                params.position,
            )
        except EmptyASTError:
            logging.warning(
                "AST for this file is empty, couldn't determine hover message.",
            )
        except Exception:
            logging.exception("DOCUMENT HOVER CRASHED.")

        return None

    def publish_diagnostics(self) -> None:
        """Publish code diagnostics for this document."""
        diagnostics: list[Diagnostic] = []
        for token in self.ast:
            diagnostics.extend(token.get_token_diagnostics())
        self.ls.publish_diagnostics(self.uri, [d.to_lspt() for d in diagnostics])
