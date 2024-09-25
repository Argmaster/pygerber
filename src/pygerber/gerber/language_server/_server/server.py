from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pygerber
from pygerber.gerber.language_server._server.document_cache import DocumentCache
from pygerber.gerber.language_server._server.documents.document import Document
from pygerber.gerber.language_server._server.documents.gerber import GerberDocument
from pygerber.gerber.language_server.status import throw_if_server_not_available

if TYPE_CHECKING:
    from pygls.server import LanguageServer


def get_server() -> LanguageServer:  # noqa: PLR0915, C901
    """Get the language server instance."""
    throw_if_server_not_available()

    import lsprotocol.types as lspt
    import pygls.server as pygls_server

    gls = pygls_server.LanguageServer(
        "pygerber.gerber.language_server",
        pygerber.__version__,
        max_workers=4,
    )
    init_params: lspt.InitializeParams = MagicMock()
    open_documents = DocumentCache()

    async def get_document(uri: str) -> Document:
        document = open_documents.get(uri)
        if document is not None:
            return document

        wrapped_uri = Path(uri)
        if wrapped_uri.match("*.g*"):
            document = GerberDocument(gls)

        else:
            msg = f"Unsupported document type: {uri!r}"
            raise NotImplementedError(msg)

        async with document:
            open_documents.set(uri, document)

        return document

    @gls.feature(lspt.INITIALIZE)
    async def _(params: lspt.InitializeParams) -> None:
        nonlocal init_params
        init_params = params

        if client_info := params.client_info:
            client_name = client_info.name
            client_version = client_info.version
        else:
            client_name = "Unknown"
            client_version = "Unknown"

        gls.show_message_log(
            "Started PyGerber's Gerber Language Server version "
            f"{pygerber.__version__} for {client_name} {client_version}.",
            lspt.MessageType.Info,
        )

    @gls.feature(lspt.TEXT_DOCUMENT_DID_OPEN)
    async def _(params: lspt.DidOpenTextDocumentParams) -> None:
        async with open_documents:
            document = await get_document(params.text_document.uri)
            await document.acquire()

        try:
            await document.on_open(params)

        finally:
            await document.release()

    @gls.feature(lspt.TEXT_DOCUMENT_DID_CLOSE)
    async def _(params: lspt.DidCloseTextDocumentParams) -> None:
        async with open_documents:
            document = await get_document(params.text_document.uri)
            await document.acquire()

            try:
                await document.on_close(params)

            finally:
                await document.release()

            open_documents.delete(params.text_document.uri)

    @gls.feature(lspt.TEXT_DOCUMENT_DID_CHANGE)
    async def _(params: lspt.DidChangeTextDocumentParams) -> None:
        async with open_documents:
            document = await get_document(params.text_document.uri)
            await document.acquire()

        try:
            await document.on_change(params)

        finally:
            await document.release()

    @gls.feature(lspt.TEXT_DOCUMENT_HOVER)
    async def _(params: lspt.HoverParams) -> lspt.Hover | None:
        async with open_documents:
            document = await get_document(params.text_document.uri)
            await document.acquire()

        try:
            hover = await document.on_hover(params)

        finally:
            await document.release()

        return hover

    @gls.feature(
        lspt.TEXT_DOCUMENT_COMPLETION,
        lspt.CompletionOptions(trigger_characters=["G", "D", "%"]),
    )
    async def _(params: lspt.CompletionParams) -> lspt.CompletionList | None:
        async with open_documents:
            document = await get_document(params.text_document.uri)
            await document.acquire()

        try:
            return await document.on_completion(params)

        finally:
            await document.release()

    return gls
