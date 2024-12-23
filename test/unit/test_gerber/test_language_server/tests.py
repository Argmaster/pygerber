from __future__ import annotations

import sys

import pytest
import pytest_lsp
from lsprotocol.types import (
    CompletionList,
    CompletionParams,
    Hover,
    HoverParams,
    InitializeParams,
    MarkupContent,
    MarkupKind,
    Position,
    TextDocumentIdentifier,
)
from pytest_lsp import (
    ClientServerConfig,
    LanguageClient,
    client_capabilities,
)

import pygerber
from test.tags import Tag, tag
from test.unit.test_gerber.common import GERBER_ASSETS_DIRECTORY


@pytest_lsp.fixture(
    config=ClientServerConfig(
        server_command=[
            sys.executable,
            "-m",
            "pygerber.gerber.language_server",
            "--quiet",
        ],
    ),
)
async def client(  # type: ignore[no-untyped-def]  # noqa: ANN201
    lsp_client: LanguageClient,
):
    # Setup
    response = await lsp_client.initialize_session(
        InitializeParams(
            capabilities=client_capabilities("visual-studio-code"),
            root_uri=(GERBER_ASSETS_DIRECTORY / "incomplete").as_uri(),
        )
    )
    assert response.server_info is not None
    assert response.server_info.version == pygerber.__version__

    yield

    # Teardown
    await lsp_client.shutdown_session()


@tag(Tag.LSP, Tag.EXTRAS)
@pytest.mark.xfail
@pytest.mark.asyncio
async def test_completion(client: LanguageClient) -> None:
    result = await client.text_document_completion_async(
        params=CompletionParams(
            position=Position(line=10, character=1),
            text_document=TextDocumentIdentifier(
                uri=(
                    GERBER_ASSETS_DIRECTORY / "incomplete" / "autocomplete_g.grb"
                ).as_uri()
            ),
        )
    )
    assert isinstance(result, CompletionList)

    assert len(result.items) > 0
    assert all(item.label.startswith("G") for item in result.items)


@tag(Tag.LSP, Tag.EXTRAS)
@pytest.mark.xfail
@pytest.mark.asyncio
async def test_hover_d01(client: LanguageClient) -> None:
    result = await client.text_document_hover_async(
        params=HoverParams(
            position=Position(line=9, character=7),
            text_document=TextDocumentIdentifier(
                uri=(
                    GERBER_ASSETS_DIRECTORY / "incomplete" / "autocomplete_g.grb"
                ).as_uri()
            ),
        )
    )
    assert isinstance(result, Hover)
    assert isinstance(result.contents, MarkupContent)
    assert result.contents.kind == MarkupKind.Markdown

    assert "## 4.8.2 Plot (D01)." in result.contents.value


@tag(Tag.LSP, Tag.EXTRAS)
@pytest.mark.xfail
@pytest.mark.asyncio
async def test_hover_invalid_expression(client: LanguageClient) -> None:
    result = await client.text_document_hover_async(
        params=HoverParams(
            position=Position(line=10, character=1),
            text_document=TextDocumentIdentifier(
                uri=(
                    GERBER_ASSETS_DIRECTORY / "incomplete" / "autocomplete_g.grb"
                ).as_uri()
            ),
        )
    )
    assert isinstance(result, Hover)
    assert isinstance(result.contents, MarkupContent)
    assert result.contents.kind == MarkupKind.Markdown

    assert "Invalid" in result.contents.value
