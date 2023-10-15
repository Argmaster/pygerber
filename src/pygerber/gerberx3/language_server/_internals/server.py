"""PyGerber's Gerber language server implementation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

import pygerber
from pygerber.common.position import Position
from pygerber.gerberx3.language_server import IS_LANGUAGE_SERVER_FEATURE_AVAILABLE
from pygerber.gerberx3.language_server._internals.error import (
    LanguageServerNotAvailableError,
)
from pygerber.gerberx3.language_server._internals.errors import EmptyASTError
from pygerber.gerberx3.language_server._internals.state import LanguageServerState

if TYPE_CHECKING:
    from pygls.server import LanguageServer


MAX_CACHE_SIZE = 64


def get_language_server() -> LanguageServer:
    """Get instance of Gerber language server."""
    if not IS_LANGUAGE_SERVER_FEATURE_AVAILABLE:
        raise LanguageServerNotAvailableError

    from lsprotocol.types import (
        INITIALIZE,
        TEXT_DOCUMENT_COMPLETION,
        TEXT_DOCUMENT_HOVER,
        CompletionItem,
        CompletionItemKind,
        CompletionList,
        CompletionOptions,
        CompletionParams,
        Hover,
        HoverParams,
        InitializeParams,
        MarkupContent,
        MarkupKind,
        MessageType,
    )
    from pygls.server import LanguageServer

    server = LanguageServer(
        "pygerber.gerberx3.language_server",
        f"v{pygerber.__version__}",
        max_workers=1,
    )

    state = LanguageServerState()

    @server.feature(INITIALIZE)
    def _initialize(params: InitializeParams) -> None:
        client_name = getattr(params.client_info, "name", "Unknown")
        client_version = getattr(params.client_info, "version", "Unknown")
        server.show_message_log(
            "Started PyGerber's Gerber Language Server version "
            f"{pygerber.__version__} for {client_name} {client_version}.",
            MessageType.Info,
        )

    @server.feature(TEXT_DOCUMENT_HOVER)
    def _text_document_hover(params: HoverParams) -> Optional[Hover]:
        try:
            ast = state.get_by_uri(params.text_document.uri).tokenize()
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

                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=token.get_hover_message(state),
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

    @server.feature(
        TEXT_DOCUMENT_COMPLETION,
        CompletionOptions(trigger_characters=["G"]),
    )
    def _text_document_completion(_params: CompletionParams) -> CompletionList:
        return CompletionList(
            is_incomplete=False,
            items=[
                CompletionItem(
                    label=f"G{code}*",
                    kind=CompletionItemKind.Keyword,
                )  # type: ignore[pylance]
                for code in [
                    "01",
                    "02",
                    "03",
                    "36",
                    "37",
                    "54",
                    "55",
                    "70",
                    "71",
                    "74",
                    "75",
                    "90",
                    "91",
                ]
            ],
        )

    return server
