"""PyGerber's Gerber language server implementation."""

from __future__ import annotations

from hashlib import sha256
from typing import TYPE_CHECKING, Optional

import pygerber
from pygerber.gerberx3.language_server import IS_LANGUAGE_SERVER_FEATURE_AVAILABLE
from pygerber.gerberx3.language_server._internals.error import (
    LanguageServerNotAvailableError,
)

if TYPE_CHECKING:
    from pygls.server import LanguageServer


MAX_CACHE_SIZE = 64


def get_language_server() -> LanguageServer:  # noqa: C901
    """Get instance of Gerber language server."""
    if not IS_LANGUAGE_SERVER_FEATURE_AVAILABLE:  # pragma: no cover
        raise LanguageServerNotAvailableError

    import lsprotocol.types as lspt
    from pygls.server import LanguageServer

    from pygerber.gerberx3.language_server._internals.document import Document

    if TYPE_CHECKING:
        from pygls import workspace

    server = LanguageServer(
        "pygerber.gerberx3.language_server",
        pygerber.__version__,
        max_workers=1,
    )

    @server.feature(lspt.INITIALIZE)
    def _initialize(params: lspt.InitializeParams) -> None:
        client_name = getattr(params.client_info, "name", "Unknown")
        client_version = getattr(params.client_info, "version", "Unknown")
        server.show_message_log(
            "Started PyGerber's Gerber Language Server version "
            f"{pygerber.__version__} for {client_name} {client_version}.",
            lspt.MessageType.Info,
        )

    @server.feature(lspt.TEXT_DOCUMENT_DID_OPEN)
    def _text_document_open(params: lspt.DidOpenTextDocumentParams) -> None:
        document = get_document(params.text_document.uri)
        document.publish_diagnostics()

    @server.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
    def _text_document_change(params: lspt.DidOpenTextDocumentParams) -> None:
        document = get_document(params.text_document.uri)
        document.publish_diagnostics()

    cached_documents_map: dict[bytes, Document] = {}

    def get_document(uri: str) -> Document:
        text_document: workspace.TextDocument = server.workspace.get_text_document(
            uri,
        )
        digest_text_document = sha256(text_document.source.encode("utf-8")).digest()
        digest_uri = sha256(text_document.uri.encode("utf-8")).digest()

        document_id = digest_text_document + digest_uri
        document = cached_documents_map.get(document_id)

        if document is None:
            if len(cached_documents_map) > MAX_CACHE_SIZE:
                cached_documents_map.popitem()

            cached_documents_map[document_id] = Document(
                server,
                text_document.source,
                uri,
            )

        return cached_documents_map[document_id]

    @server.feature(lspt.TEXT_DOCUMENT_HOVER)
    def _text_document_hover(params: lspt.HoverParams) -> Optional[lspt.Hover]:
        document = get_document(params.text_document.uri)
        return document.text_document_hover(params)

    @server.feature(
        lspt.TEXT_DOCUMENT_COMPLETION,
        lspt.CompletionOptions(trigger_characters=["G"]),
    )
    def _text_document_completion(
        _params: lspt.CompletionParams,
    ) -> lspt.CompletionList:
        return lspt.CompletionList(
            is_incomplete=False,
            items=[
                lspt.CompletionItem(
                    label=f"G{code}*",
                    kind=lspt.CompletionItemKind.Keyword,
                )
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
