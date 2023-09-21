"""PyGerber's Gerber language server implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygerber
from pygerber.gerberx3.language_server import IS_LANGUAGE_SERVER_FEATURE_AVAILABLE
from pygerber.gerberx3.language_server._internals.error import (
    LanguageServerNotAvailableError,
)

if TYPE_CHECKING:
    from pygls.server import LanguageServer


def get_language_server() -> LanguageServer:
    """Get instance of Gerber language server."""
    if not IS_LANGUAGE_SERVER_FEATURE_AVAILABLE:
        raise LanguageServerNotAvailableError

    from lsprotocol.types import (
        INITIALIZE,
        TEXT_DOCUMENT_COMPLETION,
        CompletionItem,
        CompletionItemKind,
        CompletionList,
        CompletionOptions,
        CompletionParams,
        InitializeParams,
        MessageType,
    )
    from pygls.server import LanguageServer

    server = LanguageServer(
        "pygerber.gerberx3.language_server",
        f"v{pygerber.__version__}",
    )

    @server.feature(INITIALIZE)
    def _initialize(params: InitializeParams) -> None:
        client_name = getattr(params.client_info, "name", "Unknown")
        client_version = getattr(params.client_info, "version", "Unknown")
        server.show_message_log(
            "Started PyGerber's Gerber Language Server version "
            f"{pygerber.__version__} for {client_name} {client_version}.",
            MessageType.Info,
        )

    @server.feature(
        TEXT_DOCUMENT_COMPLETION,
        CompletionOptions(trigger_characters=["G"]),
    )
    def _text_document_completion(_params: CompletionParams) -> CompletionList:
        server.show_message_log("heh")

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
